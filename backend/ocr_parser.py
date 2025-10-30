import re
import mysql.connector
from datetime import datetime, timedelta
import mysql.connector

class OCRPrescriptionParser:
    def __init__(self):
        self.medicine_patterns = [
            r'(?:Tab|Tablet|Cap|Capsule|Syrup|Injection)\s+([A-Za-z\s]+)\s+(\d+(?:\.\d+)?)\s*(?:mg|ml|g)',
            r'([A-Za-z\s]+)\s+(\d+(?:\.\d+)?)\s*(?:mg|ml|g)',
            r'(\w+)\s+(?:tablet|cap|syrup)',
        ]
        
    def parse_text_input(self, text):
        medicines = []
        lines = text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            for pattern in self.medicine_patterns:
                matches = re.findall(pattern, line, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        name = match[0].strip()
                        dosage = f"{match[1]}mg" if len(match) > 1 else "As prescribed"
                    else:
                        name = match.strip()
                        dosage = "As prescribed"
                    
                    if len(name) > 2:
                        medicines.append({
                            'name': name,
                            'dosage': dosage,
                            'frequency': 'As prescribed'
                        })
        
        return medicines
    
    def save_to_database(self, user_id, medicines):
        try:
            conn = mysql.connector.connect(
                host='localhost', user='root',
                password='root@123', database='meditrack'
            )
            cursor = conn.cursor()
            
            saved_count = 0
            for med in medicines:
                cursor.execute("""
                    INSERT INTO medicines (user_id, name, dosage, frequency, created_at)
                    VALUES (%s, %s, %s, %s, %s)
                """, (user_id, med['name'], med['dosage'], med['frequency'], datetime.now()))
                saved_count += 1
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return {'success': True, 'count': saved_count}
        except Exception as e:
            return {'success': False, 'error': str(e)}