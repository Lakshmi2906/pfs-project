from datetime import datetime, timedelta
import mysql.connector

class MedicineScheduler:
    def __init__(self):
        self.time_slots = {
            1: ['08:00'],
            2: ['08:00', '20:00'],
            3: ['08:00', '14:00', '20:00'],
            4: ['08:00', '12:00', '16:00', '20:00']
        }
    
    def schedule_medicine(self, user_id, medicine_name, dosage, times_per_day, duration_days):
        try:
            conn = mysql.connector.connect(
                host='localhost', user='root',
                password='root@123', database='meditrack'
            )
            cursor = conn.cursor()
            
            start_date = datetime.now().date()
            next_dose = datetime.combine(start_date, datetime.strptime(self.time_slots[times_per_day][0], '%H:%M').time())
            
            cursor.execute("""
                INSERT INTO medicines (user_id, name, dosage, frequency, times_per_day, 
                                     duration_days, start_date, next_dose, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (user_id, medicine_name, dosage, f"{times_per_day}x daily", 
                  times_per_day, duration_days, start_date, next_dose, datetime.now()))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return {'success': True, 'message': 'Medicine scheduled successfully'}
        except Exception as e:
            return {'success': False, 'error': str(e)}