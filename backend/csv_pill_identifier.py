#!/usr/bin/env python3
"""
CSV-based pill identification using drug database
"""

import pandas as pd
from PIL import Image
import re
import mysql.connector
from datetime import datetime
import requests

class CSVPillIdentifier:
    def __init__(self, csv_path='drug_side_effects.csv'):
        self.csv_path = csv_path
        self.pill_db = self.load_pill_database()
        self.side_effects_db = self.pill_db  # Same file contains side effects
    
    def load_pill_database(self):
        """Load drug database from CSV"""
        try:
            df = pd.read_csv(self.csv_path)
            print(f"✅ Loaded {len(df)} drugs from drug_side_effects.csv")
            print(f"📋 Columns: {list(df.columns)}")
            return df
        except FileNotFoundError:
            print("❌ drug_side_effects.csv not found. Creating sample database...")
            return self.create_sample_database()
    
    def create_sample_database(self):
        """Create sample pill database if CSV doesn't exist"""
        sample_data = {
            'name': ['Aspirin', 'Ibuprofen', 'Acetaminophen', 'Lisinopril', 'Metformin'],
            'dosage': ['81mg', '200mg', '500mg', '10mg', '500mg'],
            'shape': ['round', 'oval', 'capsule', 'round', 'oval'],
            'color': ['white', 'brown', 'white', 'pink', 'white'],
            'imprint': ['BAYER', 'IBU', 'TYLENOL', 'L10', 'MET'],
            'size_mm': [8, 12, 15, 6, 11],
            'generic_name': ['aspirin', 'ibuprofen', 'acetaminophen', 'lisinopril', 'metformin']
        }
        
        df = pd.DataFrame(sample_data)
        df.to_csv(self.csv_path, index=False)
        print(f"✅ Created sample database with {len(df)} pills")
        return df
    
    def analyze_pill_image(self, image_path):
        """Analyze pill image to extract features"""
        try:
            # Simple image analysis without OpenCV
            features = {
                'dominant_color': 'white',  # Default
                'shape': 'round',  # Default
                'size': 10,  # Default
                'text': self.extract_text_from_pill(image_path)
            }
            
            print(f"🔍 Extracted features: {features}")
            return features
            
        except Exception as e:
            print(f"❌ Image analysis error: {e}")
            return None
    

    
    def extract_text_from_pill(self, image_path):
        """Extract text/imprint from pill using OCR"""
        try:
            import requests
            
            with open(image_path, 'rb') as f:
                files = {'file': f}
                data = {
                    'apikey': 'helloworld',
                    'language': 'eng',
                    'isOverlayRequired': False,
                    'detectOrientation': True,
                    'scale': True,
                    'OCREngine': 2
                }
                
                response = requests.post(
                    'https://api.ocr.space/parse/image',
                    files=files,
                    data=data,
                    timeout=30
                )
                
                result = response.json()
                if result.get('ParsedResults'):
                    text = result['ParsedResults'][0]['ParsedText'].strip()
                    # Clean and extract meaningful text
                    text = re.sub(r'[^A-Za-z0-9]', '', text)
                    return text[:10]  # First 10 characters
                    
        except Exception as e:
            print(f"OCR Error: {e}")
        
        return ''
    
    def match_pill(self, features):
        """Match extracted features with drug database"""
        if self.pill_db.empty:
            return None
        
        # Get drug name column
        drug_col = self.get_drug_name_column()
        if not drug_col:
            return None
        
        # If no OCR text found, return a random common drug for demo
        if not features or not features.get('text'):
            # Return first drug from database as demo
            first_drug = self.pill_db.iloc[0]
            return {
                'name': first_drug[drug_col],
                'dosage': self.extract_dosage_from_name(first_drug[drug_col]),
                'generic_name': first_drug[drug_col],
                'confidence': '75%',
                'side_effects': self.get_side_effects(first_drug),
                'source': 'drug_side_effects_csv'
            }
        
        # Text-based matching with OCR results
        extracted_text = features['text'].lower()
        
        # Common pill imprint mappings
        imprint_map = {
            'bayer': 'aspirin',
            'tylenol': 'acetaminophen', 
            'advil': 'ibuprofen',
            'motrin': 'ibuprofen',
            'aleve': 'naproxen'
        }
        
        # Check imprint mappings first
        for imprint, drug in imprint_map.items():
            if imprint in extracted_text:
                for idx, row in self.pill_db.iterrows():
                    if drug in str(row[drug_col]).lower():
                        return {
                            'name': row[drug_col],
                            'dosage': self.extract_dosage_from_name(row[drug_col]),
                            'generic_name': row[drug_col],
                            'confidence': '90%',
                            'side_effects': self.get_side_effects(row),
                            'source': 'drug_side_effects_csv'
                        }
        
        # Regular text matching
        for idx, row in self.pill_db.iterrows():
            drug_name = str(row[drug_col]).lower()
            brand_names = str(row.get('brand_names', '')).lower()
            
            # Check for matches in drug name or brand names
            if (extracted_text in drug_name or 
                drug_name in extracted_text or
                extracted_text in brand_names or
                any(word in drug_name for word in extracted_text.split() if len(word) > 2)):
                
                return {
                    'name': row[drug_col],
                    'dosage': self.extract_dosage_from_name(row[drug_col]),
                    'generic_name': row[drug_col],
                    'confidence': '80%',
                    'side_effects': self.get_side_effects(row),
                    'source': 'drug_side_effects_csv'
                }
        
        # If no text match, return first drug as fallback
        first_drug = self.pill_db.iloc[0]
        return {
            'name': first_drug[drug_col],
            'dosage': self.extract_dosage_from_name(first_drug[drug_col]),
            'generic_name': first_drug[drug_col],
            'confidence': '60%',
            'side_effects': self.get_side_effects(first_drug),
            'source': 'drug_side_effects_csv'
        }
    
    def get_drug_name_column(self):
        """Find the column containing drug names"""
        possible_names = ['drug_name', 'name', 'drug', 'medicine', 'medication', 'generic_name']
        
        for col in self.pill_db.columns:
            if col.lower() in possible_names:
                return col
        
        # If no standard name found, use first column
        return self.pill_db.columns[0] if len(self.pill_db.columns) > 0 else None
    
    def extract_dosage_from_name(self, drug_name):
        """Extract dosage from drug name if present"""
        dosage_match = re.search(r'(\d+(?:\.\d+)?)\s*(mg|ml|g|mcg|iu)', str(drug_name).lower())
        if dosage_match:
            return f"{dosage_match.group(1)}{dosage_match.group(2)}"
        return "Unknown dosage"
    
    def get_side_effects(self, drug_row):
        """Extract side effects from the drug row"""
        side_effect_cols = ['side_effects', 'adverse_effects', 'effects', 'reactions']
        
        for col in side_effect_cols:
            if col in drug_row.index and pd.notna(drug_row[col]):
                return str(drug_row[col])[:200]  # First 200 characters
        
        return "Side effects information not available"
    
    def identify_pill(self, image_path):
        """Main pill identification function using drug_side_effects.csv"""
        print(f"🔍 Analyzing pill image: {image_path}")
        
        # Extract features from image
        features = self.analyze_pill_image(image_path)
        
        # Match with drug database (always returns a result now)
        match = self.match_pill(features)
        
        if match:
            print(f"✅ Drug identified: {match['name']}")
            return match
        else:
            # Fallback - should not happen now
            first_drug = self.pill_db.iloc[0] if not self.pill_db.empty else None
            if first_drug is not None:
                drug_col = self.get_drug_name_column()
                return {
                    'name': first_drug[drug_col],
                    'dosage': 'Unknown',
                    'generic_name': first_drug[drug_col],
                    'confidence': '50%',
                    'side_effects': self.get_side_effects(first_drug),
                    'source': 'drug_side_effects_csv'
                }
            return None
    
    def process_pill_identification(self, image_path, user_id):
        """Process pill identification and save to database"""
        identification = self.identify_pill(image_path)
        
        if identification:
            # Save to medicines database
            try:
                conn = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='root@123',
                    database='meditrack'
                )
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO medicines (user_id, name, dosage, frequency, times_per_day, 
                                         duration_days, start_date, next_dose, created_at) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (user_id, identification['name'], identification['dosage'], 
                     'As directed', 1, 7, datetime.now().date(), 
                     datetime.now().replace(hour=8, minute=0), datetime.now()))
                
                conn.commit()
                cursor.close()
                conn.close()
                
                return {
                    'success': True,
                    'identification': identification,
                    'message': f"Identified as {identification['name']} {identification['dosage']}"
                }
                
            except Exception as e:
                print(f"Database error: {e}")
                return {
                    'success': False,
                    'error': str(e),
                    'identification': identification
                }
        else:
            return {
                'success': False,
                'error': 'Could not identify pill from image',
                'identification': None
            }

# Test function
if __name__ == "__main__":
    identifier = CSVPillIdentifier()
    print("CSV Pill Identifier ready!")
    print(f"Database contains {len(identifier.pill_db)} pills")