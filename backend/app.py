from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import hashlib
import time
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
# Enhanced CORS configuration
CORS(app, origins=['http://localhost:3000'], 
     methods=['GET', 'POST', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization'])

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone', '')  # Optional phone number
        
        hashed = hashlib.sha256(password.encode()).hexdigest()
        
        conn = mysql.connector.connect(
            host='localhost', user='root', 
            password='root@123', database='meditrack'
        )
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, password, phone) VALUES (%s, %s, %s, %s)", 
                      (name, email, hashed, phone))
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'User registered'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        print(f"Login request received from {request.remote_addr}")
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        print(f"Attempting login for: {email}")
        
        conn = mysql.connector.connect(
            host='localhost', user='root',
            password='root@123', database='meditrack'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not user:
            print(f"User not found: {email}")
            return jsonify({'error': 'User not found'}), 401
            
        input_hash = hashlib.sha256(password.encode()).hexdigest()
        print(f"Password check - Input: {input_hash[:10]}... Stored: {user[2][:10]}...")
        
        if input_hash == user[2]:
            token = hashlib.md5(f"{user[0]}{time.time()}".encode()).hexdigest()
            print(f"Login successful for user {user[0]}")
            return jsonify({'token': token, 'user': {'id': user[0], 'name': user[1]}}), 200
        
        print("Password mismatch")
        return jsonify({'error': 'Wrong password'}), 401
        
    except mysql.connector.Error as db_error:
        print(f"Database error: {db_error}")
        return jsonify({'error': 'Database connection failed'}), 500
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/medicines', methods=['GET'])
def get_medicines():
    try:
        user_id = request.args.get('user_id', 1)
        print(f"Fetching medicines for user {user_id}")
        
        conn = mysql.connector.connect(
            host='localhost', user='root',
            password='root@123', database='meditrack'
        )
        cursor = conn.cursor()
        
        # Debug: Check all medicines first
        cursor.execute("SELECT COUNT(*) FROM medicines")
        total_count = cursor.fetchone()[0]
        print(f"Total medicines in database: {total_count}")
        
        cursor.execute("SELECT user_id, name, dosage FROM medicines")
        all_medicines = cursor.fetchall()
        print(f"All medicines: {all_medicines}")
        
        # Now get medicines for specific user
        cursor.execute("""
            SELECT id, name, dosage, frequency, times_per_day, duration_days, 
                   start_date, next_dose, created_at 
            FROM medicines WHERE user_id = %s ORDER BY created_at DESC
        """, (user_id,))
        medicines = cursor.fetchall()
        cursor.close()
        conn.close()
        
        print(f"Found {len(medicines)} medicines for user {user_id}")
        
        result = []
        for med in medicines:
            result.append({
                'id': med[0],
                'name': med[1],
                'dosage': med[2],
                'frequency': med[3],
                'times_per_day': med[4],
                'duration_days': med[5],
                'start_date': str(med[6]) if med[6] else None,
                'next_dose': str(med[7]) if med[7] else None,
                'created_at': str(med[8]) if med[8] else None
            })
        
        print(f"Returning medicines: {result}")
        return jsonify(result), 200
    except Exception as e:
        print(f"Error fetching medicines: {e}")
        return jsonify([]), 200

@app.route('/api/reminders', methods=['GET'])
def get_reminders():
    try:
        user_id = request.args.get('user_id', 1)
        
        conn = mysql.connector.connect(
            host='localhost', user='root',
            password='root@123', database='meditrack'
        )
        cursor = conn.cursor()
        
        # Get medicines and generate reminders from scheduling info
        cursor.execute("""
            SELECT id, name, dosage, times_per_day, next_dose
            FROM medicines WHERE user_id = %s
        """, (user_id,))
        
        medicines = cursor.fetchall()
        cursor.close()
        conn.close()
        
        result = []
        for med in medicines:
            medicine_id, name, dosage, times_per_day, _ = med
            
            # Generate reminder times based on times_per_day
            if times_per_day == 1:
                times = ['8:00 AM']
            elif times_per_day == 2:
                times = ['8:00 AM', '8:00 PM']
            elif times_per_day == 3:
                times = ['8:00 AM', '2:00 PM', '8:00 PM']
            else:
                times = ['8:00 AM']
            
            for time_str in times:
                result.append({
                    'id': f"{medicine_id}_{time_str}",
                    'medicine_id': medicine_id,
                    'medicine_name': name,
                    'dosage': dosage,
                    'reminder_time': time_str,
                    'status': 'pending'
                })
        
        return jsonify(result), 200
    except Exception as e:
        print(f"Error fetching reminders: {e}")
        return jsonify([]), 200



@app.route('/api/upload-prescription', methods=['POST'])
def upload_prescription():
    try:
        print("=== UPLOAD REQUEST RECEIVED ===")
        
        if 'file' not in request.files:
            print("ERROR: No file in request")
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        user_id = request.form.get('user_id', 1)
        upload_type = request.form.get('type', 'prescription')  # prescription or pill
        
        print(f"File: {file.filename}, User ID: {user_id}, Type: {upload_type}")
        
        if file.filename == '':
            print("ERROR: Empty filename")
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(f"Saving file to: {filepath}")
            file.save(filepath)
            
            if upload_type == 'pill':
                # Process pill identification with ML model
                print("Starting ML-based pill identification...")
                from ml_pill_identifier import MLPillIdentifier
                identifier = MLPillIdentifier()
                result = identifier.identify_pill(filepath, user_id)
            else:
                # Process prescription
                print("Starting prescription processing...")
                from prescription_parser import PrescriptionParser
                parser = PrescriptionParser()
                result = parser.process_prescription(filepath, user_id)
            
            print(f"Processing result: {result}")
            
            # Clean up uploaded file
            os.remove(filepath)
            print("File cleaned up")
            
            return jsonify(result)
        else:
            print(f"ERROR: Invalid file type: {file.filename}")
            return jsonify({'success': False, 'error': 'Invalid file type'}), 400
            
    except Exception as e:
        print(f"EXCEPTION in upload_prescription: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/parse-text', methods=['POST'])
def parse_text():
    try:
        from ocr_parser import OCRPrescriptionParser
        
        data = request.get_json()
        prescription_text = data.get('text', '')
        user_id = data.get('user_id', 1)
        
        parser = OCRPrescriptionParser()
        medicines = parser.parse_text_input(prescription_text)
        result = parser.save_to_database(user_id, medicines)
        
        return jsonify({
            'success': result['success'],
            'medicines': medicines,
            'saved_count': result.get('count', 0)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/api/update-phone', methods=['POST'])
def update_phone():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        phone = data.get('phone')
        
        conn = mysql.connector.connect(
            host='localhost', user='root',
            password='root@123', database='meditrack'
        )
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET phone = %s WHERE id = %s", (phone, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Phone number updated'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/trusted-call', methods=['POST'])
def make_trusted_call():
    try:
        from trusted_call_agent import TrustedCallAgent
        
        data = request.get_json()
        user_id = data.get('user_id')
        medicine_id = data.get('medicine_id')
        
        agent = TrustedCallAgent()
        success = agent.make_trusted_call(user_id, medicine_id)
        
        return jsonify({'success': success}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/call-response', methods=['POST'])
def handle_call_response():
    try:
        from trusted_call_agent import TrustedCallAgent
        
        data = request.form
        user_id = data.get('user_id')
        medicine_id = data.get('medicine_id')
        digits = data.get('Digits')
        
        agent = TrustedCallAgent()
        agent.handle_call_response(user_id, medicine_id, digits)
        
        return '<Response><Say>Thank you!</Say></Response>', 200
    except Exception:
        return '<Response><Say>Error occurred</Say></Response>', 500



@app.route('/api/debug-medicines', methods=['GET'])
def debug_medicines():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root@123',
            database='meditrack'
        )
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM medicines")
        medicines = cursor.fetchall()
        cursor.close()
        conn.close()
        
        result = []
        for med in medicines:
            result.append({
                'id': med[0],
                'user_id': med[1],
                'name': med[2],
                'dosage': med[3],
                'frequency': med[4],
                'next_dose': med[5] if len(med) > 5 else None,
                'created_at': str(med[6]) if len(med) > 6 else None
            })
        
        return jsonify({'medicines': result, 'count': len(result)}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting MediTrack backend server...")
    print("Server will run on: http://localhost:5000")
    print("Frontend should connect to: http://localhost:5000/api/")
    app.run(host='0.0.0.0', port=5000, debug=True)