import mysql.connector
import requests
from datetime import datetime

class TrustedCallAgent:
    def __init__(self):
        self.n8n_webhook_url = "http://localhost:5678/webhook/medicine-reminder"
    
    def make_trusted_call(self, user_id, medicine_id):
        try:
            conn = mysql.connector.connect(
                host='localhost', user='root',
                password='root@123', database='meditrack'
            )
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT u.name, u.phone, m.name, m.dosage 
                FROM users u JOIN medicines m ON u.id = m.user_id 
                WHERE u.id = %s AND m.id = %s
            """, (user_id, medicine_id))
            
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if result:
                user_name, phone, medicine_name, dosage = result
                
                payload = {
                    'user_id': user_id,
                    'user_name': user_name,
                    'phone': phone,
                    'medicine_name': medicine_name,
                    'dosage': dosage,
                    'timestamp': datetime.now().isoformat()
                }
                
                response = requests.post(self.n8n_webhook_url, json=payload, timeout=10)
                return response.status_code == 200
            
            return False
        except Exception as e:
            print(f"Call error: {e}")
            return False
    
    def handle_call_response(self, user_id, medicine_id, digits):
        if digits == '1':
            print(f"User {user_id} confirmed taking medicine {medicine_id}")
        elif digits == '2':
            print(f"User {user_id} will take medicine {medicine_id} later")
        else:
            print(f"User {user_id} gave unclear response: {digits}")