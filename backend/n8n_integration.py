import requests
import json
from datetime import datetime

class N8NIntegration:
    def __init__(self):
        self.webhook_url = "http://localhost:5678/webhook/medicine-reminder"
        self.timeout = 10
    
    def send_reminder_webhook(self, user_data, medicine_data):
        try:
            payload = {
                'user_id': user_data.get('id'),
                'user_name': user_data.get('name'),
                'phone': user_data.get('phone'),
                'medicine_name': medicine_data.get('name'),
                'dosage': medicine_data.get('dosage'),
                'reminder_time': medicine_data.get('reminder_time'),
                'timestamp': datetime.now().isoformat(),
                'action': 'medicine_reminder'
            }
            
            response = requests.post(
                self.webhook_url, 
                json=payload, 
                timeout=self.timeout,
                headers={'Content-Type': 'application/json'}
            )
            
            return {
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'response': response.text
            }
            
        except requests.exceptions.Timeout:
            return {'success': False, 'error': 'Webhook timeout'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def send_prescription_analysis(self, user_id, medicines_list):
        try:
            payload = {
                'user_id': user_id,
                'medicines': medicines_list,
                'timestamp': datetime.now().isoformat(),
                'action': 'prescription_analysis'
            }
            
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=self.timeout
            )
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"N8N integration error: {e}")
            return False