import re
import mysql.connector
from datetime import datetime
import requests

class PrescriptionParser:
    def __init__(self):
        pass

    def extract_text_from_image(self, image_path):
        """Extract text using online OCR"""
        try:
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
                    return result['ParsedResults'][0]['ParsedText']
                return ""
        except Exception as e:
            print(f"OCR Error: {e}")
            return ""

    def parse_medicines(self, text):
        """Simple medicine extraction"""
        medicines = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if len(line) < 5:
                continue
            
            # Look for medicine patterns
            medicine_match = re.search(r'(?i)(rx\s+)?([a-z]+(?:\s+[a-z]+)*)\s+(\d+)\s*(mg|ml|g|iu|mcg)', line)
            if medicine_match:
                name = medicine_match.group(2).strip().title()
                dosage = f"{medicine_match.group(3)}{medicine_match.group(4)}"
                
                medicine = {
                    'name': name,
                    'dosage': dosage,
                    'frequency': 'As directed'
                }
                medicines.append(medicine)
                print(f"Found medicine: {medicine}")
        
        return medicines

    def save_to_database(self, user_id, medicines):
        """Save medicines to database with scheduling"""
        try:
            print(f"Connecting to database for user {user_id}...")
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root@123',
                database='meditrack'
            )
            cursor = conn.cursor()
            print("Database connected successfully")
            
            saved_count = 0
            for medicine in medicines:
                print(f"Inserting medicine: {medicine}")
                
                # Extract scheduling info
                times_per_day = self.extract_times_per_day(medicine['frequency'])
                duration_days = self.extract_duration(medicine.get('instructions', ''))
                next_dose = self.calculate_next_dose(times_per_day)
                
                cursor.execute("""
                    INSERT INTO medicines (user_id, name, dosage, frequency, times_per_day, 
                                         duration_days, start_date, next_dose, created_at) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (user_id, medicine['name'], medicine['dosage'], 
                     medicine['frequency'], times_per_day, duration_days,
                     datetime.now().date(), next_dose, datetime.now()))
                
                medicine_id = cursor.lastrowid
                print(f"Medicine saved with ID: {medicine_id}")
                # Reminders handled by automatic service via n8n
                
                saved_count += 1
                print(f"Medicine and schedule created successfully")
            
            conn.commit()
            print(f"Transaction committed. {saved_count} medicines saved.")
            cursor.close()
            conn.close()
            
            return {'success': True, 'count': saved_count}
        except Exception as e:
            print(f"Database Error: {e}")
            return {'success': False, 'error': str(e)}

    def save_prescription_record(self, user_id, filename, file_path):
        """Save prescription upload record"""
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root@123',
                database='meditrack'
            )
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO prescriptions (user_id, filename, file_path, upload_date) 
                VALUES (%s, %s, %s, %s)
            """, (user_id, filename, file_path, datetime.now()))
            
            conn.commit()
            cursor.close()
            conn.close()
            print(f"Prescription record saved: {filename}")
            
        except Exception as e:
            print(f"Failed to save prescription record: {e}")
    
    def extract_times_per_day(self, frequency):
        """Extract times per day from frequency text"""
        freq_lower = frequency.lower()
        if 'twice' in freq_lower or '2x' in freq_lower or 'two times' in freq_lower:
            return 2
        elif 'thrice' in freq_lower or '3x' in freq_lower or 'three times' in freq_lower:
            return 3
        elif 'four times' in freq_lower or '4x' in freq_lower:
            return 4
        else:
            return 1
    
    def extract_duration(self, text):
        """Extract duration in days"""
        import re
        duration_match = re.search(r'(\d+)\s*days?', text.lower())
        if duration_match:
            return int(duration_match.group(1))
        return 7  # Default 7 days
    
    def calculate_next_dose(self, times_per_day):
        """Calculate next dose time"""
        from datetime import datetime, timedelta, time
        now = datetime.now()
        
        if times_per_day == 1:
            next_dose = now.replace(hour=8, minute=0, second=0, microsecond=0)
        elif times_per_day == 2:
            morning = now.replace(hour=8, minute=0, second=0, microsecond=0)
            evening = now.replace(hour=20, minute=0, second=0, microsecond=0)
            next_dose = morning if now < morning else evening
        elif times_per_day == 3:
            times = [8, 14, 20]
            for hour in times:
                dose_time = now.replace(hour=hour, minute=0, second=0, microsecond=0)
                if now < dose_time:
                    next_dose = dose_time
                    break
            else:
                next_dose = now.replace(hour=8, minute=0, second=0, microsecond=0) + timedelta(days=1)
        else:
            next_dose = now + timedelta(hours=8)
        
        if next_dose <= now:
            next_dose += timedelta(days=1)
        
        return next_dose
    
    def create_simple_reminders(self, cursor, medicine_id, user_id, times_per_day):
        """Create simple reminders for medicine"""
        from datetime import datetime, time
        
        today = datetime.now().date()
        
        if times_per_day == 1:
            reminder_times = [datetime.combine(today, time(8, 0))]
        elif times_per_day == 2:
            reminder_times = [datetime.combine(today, time(8, 0)), datetime.combine(today, time(20, 0))]
        elif times_per_day == 3:
            reminder_times = [datetime.combine(today, time(8, 0)), datetime.combine(today, time(14, 0)), datetime.combine(today, time(20, 0))]
        else:
            reminder_times = [datetime.combine(today, time(8, 0))]
        
        for reminder_time in reminder_times:
            cursor.execute("""
                INSERT INTO reminders (medicine_id, user_id, reminder_time, status)
                VALUES (%s, %s, %s, 'pending')
            """, (medicine_id, user_id, reminder_time))
    
    def process_prescription(self, image_path, user_id):
        """Process prescription image with scheduling"""
        import os
        filename = os.path.basename(image_path)
        
        # Save prescription record
        self.save_prescription_record(user_id, filename, image_path)
        
        text = self.extract_text_from_image(image_path)
        print(f"Extracted text: {text}")
        
        medicines = self.parse_medicines(text)
        print(f"Found {len(medicines)} medicines")
        
        result = self.save_to_database(user_id, medicines)
        
        # Send to n8n if available
       
        
        return {
            'success': result['success'],
            'medicines': medicines,
            'saved_count': result.get('count', 0),
            'raw_text': text,
            'schedules_created': result.get('count', 0),
            'error': result.get('error')
        }