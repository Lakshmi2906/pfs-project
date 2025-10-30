import mysql.connector
import requests
from datetime import datetime, time
import schedule
import threading

class AutomaticReminderService:
    def __init__(self):
        self.n8n_webhook_url = "http://localhost:5678/webhook/medicine-reminder"
        self.call_times = {
            1: [time(8, 0)],
            2: [time(8, 0), time(20, 0)],
            3: [time(8, 0), time(14, 0), time(20, 0)],
            4: [time(8, 0), time(12, 0), time(16, 0), time(20, 0)]
        }
    
    def check_and_call_users(self):
        try:
            current_time = datetime.now().time()
            current_hour_minute = time(current_time.hour, current_time.minute)
            
            conn = mysql.connector.connect(
                host='localhost', user='root',
                password='root@123', database='meditrack'
            )
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT DISTINCT u.id, u.name, u.phone, m.id, m.name, m.dosage, m.times_per_day
                FROM users u JOIN medicines m ON u.id = m.user_id 
                WHERE u.phone IS NOT NULL AND u.phone != ''
            """)
            
            users_medicines = cursor.fetchall()
            cursor.close()
            conn.close()
            
            for user_id, user_name, phone, med_id, med_name, dosage, times_per_day in users_medicines:
                if times_per_day in self.call_times:
                    scheduled_times = self.call_times[times_per_day]
                    
                    for scheduled_time in scheduled_times:
                        if (scheduled_time.hour == current_hour_minute.hour and 
                            scheduled_time.minute == current_hour_minute.minute):
                            
                            self.make_call(user_id, user_name, phone, med_name, dosage)
                            
        except Exception as e:
            print(f"Error in check_and_call_users: {e}")
    
    def make_call(self, user_id, user_name, phone, medicine_name, dosage):
        try:
            payload = {
                'user_id': user_id,
                'user_name': user_name,
                'phone': phone,
                'medicine_name': medicine_name,
                'dosage': dosage,
                'timestamp': datetime.now().isoformat(),
                'call_type': 'automatic_reminder'
            }
            
            response = requests.post(self.n8n_webhook_url, json=payload, timeout=5)
            print(f"Called {user_name} for {medicine_name}: {response.status_code}")
            
        except Exception as e:
            print(f"Failed to call {user_name}: {e}")
    
    def start_service(self):
        schedule.every().minute.do(self.check_and_call_users)
        
        def run_scheduler():
            while True:
                schedule.run_pending()
                
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        print("Automatic reminder service started")

if __name__ == "__main__":
    service = AutomaticReminderService()
    service.start_service()
    
    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Service stopped")