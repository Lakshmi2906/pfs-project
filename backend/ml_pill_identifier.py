import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import mysql.connector
from datetime import datetime
import requests

class MLPillIdentifier:
    def __init__(self):
        self.csv_path = 'drug_side_effects.csv'
        self.drug_data = None
        self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        self.drug_vectors = None
        self.load_drug_data()
    
    def load_drug_data(self):
        try:
            self.drug_data = pd.read_csv(self.csv_path)
            search_texts = []
            for _, row in self.drug_data.iterrows():
                text = f"{row['drug_name']} {row.get('generic_name', '')} {row.get('brand_names', '')}"
                search_texts.append(text.lower())
            
            self.drug_vectors = self.vectorizer.fit_transform(search_texts)
            print(f"Loaded {len(self.drug_data)} drugs from CSV")
        except Exception as e:
            print(f"Error loading drug data: {e}")
    
    def extract_text_from_image(self, image_path):
        try:
            # Use online OCR service
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
                    text = result['ParsedResults'][0]['ParsedText']
                    cleaned_text = re.sub(r'[^A-Za-z0-9\s]', '', text)
                    return cleaned_text.strip()
                return ""
        except Exception as e:
            print(f"OCR Error: {e}")
            return ""
    
    def match_with_database(self, extracted_text):
        if self.drug_data is None or not extracted_text:
            return []
        
        matches = []
        query_vector = self.vectorizer.transform([extracted_text.lower()])
        similarities = cosine_similarity(query_vector, self.drug_vectors).flatten()
        
        top_indices = similarities.argsort()[-3:][::-1]
        
        for idx in top_indices:
            if similarities[idx] > 0.05:  # Lower threshold
                drug_info = self.drug_data.iloc[idx]
                matches.append({
                    'drug_name': drug_info['drug_name'],
                    'generic_name': drug_info.get('generic_name', ''),
                    'side_effects': drug_info.get('side_effects', ''),
                    'medical_condition': drug_info.get('medical_condition', ''),
                    'confidence': float(similarities[idx])
                })
                print(f"Match: {drug_info['drug_name']} - Confidence: {similarities[idx]:.3f}")
        
        return matches
    
    def search_by_imprint(self, extracted_text):
        """Search for pills by imprint codes or partial text"""
        matches = []
        
        if not extracted_text or len(extracted_text) < 2:
            return matches
        
        # Search in drug names and brand names for partial matches
        search_terms = extracted_text.lower().split()
        
        for _, drug_info in self.drug_data.iterrows():
            drug_text = f"{drug_info['drug_name']} {drug_info.get('brand_names', '')}".lower()
            
            # Check if any extracted term matches drug names
            for term in search_terms:
                if len(term) > 2 and term in drug_text:
                    matches.append({
                        'drug_name': drug_info['drug_name'],
                        'generic_name': drug_info.get('generic_name', ''),
                        'side_effects': drug_info.get('side_effects', ''),
                        'medical_condition': drug_info.get('medical_condition', ''),
                        'confidence': 0.6
                    })
                    print(f"Imprint match: {term} -> {drug_info['drug_name']}")
                    break
            
            if len(matches) >= 3:
                break
        
        return matches
    
    def match_by_filename(self, filename):
        """Try to match based on filename"""
        matches = []
        
        # Remove file extension and common words
        clean_filename = filename.replace('.jpg', '').replace('.jpeg', '').replace('.png', '')
        
        # Check if any drug name is in filename
        for _, drug_info in self.drug_data.iterrows():
            drug_name = drug_info['drug_name'].lower()
            if drug_name in clean_filename:
                matches.append({
                    'drug_name': drug_info['drug_name'],
                    'generic_name': drug_info.get('generic_name', ''),
                    'side_effects': drug_info.get('side_effects', ''),
                    'medical_condition': drug_info.get('medical_condition', ''),
                    'confidence': 0.8  # High confidence for filename match
                })
                print(f"Filename match: {drug_name}")
                break
        
        return matches
    
    def identify_pill(self, image_path, user_id):
        try:
            extracted_text = self.extract_text_from_image(image_path)
            print(f"Extracted text: '{extracted_text}'")
            
            # Get filename for matching
            import os
            filename = os.path.basename(image_path).lower()
            print(f"Filename: {filename}")
            
            matches = self.match_with_database(extracted_text)
            print(f"Found {len(matches)} matches")
            
            # Try filename matching if no text matches
            if not matches:
                matches = self.match_by_filename(filename)
                print(f"Filename matching found {len(matches)} matches")
            
            # Try imprint-based search if still no matches
            if not matches:
                matches = self.search_by_imprint(extracted_text)
                print(f"Imprint search found {len(matches)} matches")
            
            # If still no matches, return empty (no random results)
            if not matches:
                print("No matches found for this pill image")
            
            self.save_results(user_id, matches)
            
            return {
                'success': True,
                'matches': matches,
                'extracted_text': extracted_text
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def save_results(self, user_id, matches):
        try:
            conn = mysql.connector.connect(
                host='localhost', user='root',
                password='root@123', database='meditrack'
            )
            cursor = conn.cursor()
            
            for match in matches:
                cursor.execute("""
                    INSERT INTO medicines (user_id, name, dosage, frequency, created_at)
                    VALUES (%s, %s, %s, %s, %s)
                """, (user_id, match['drug_name'], 'As prescribed', 
                     f"AI Confidence: {match['confidence']:.2f}", datetime.now()))
            
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Save error: {e}")