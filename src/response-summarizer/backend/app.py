from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Default Ollama API endpoint

# Database initialization
def init_db():
    conn = sqlite3.connect('responses.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            response_text TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database when the application starts
init_db()

def get_db_connection():
    conn = sqlite3.connect('responses.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/submit_response', methods=['POST'])
def submit_response():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'student_id' not in data or 'response_text' not in data:
            return jsonify({
                'error': 'Missing required fields. Please provide student_id and response_text'
            }), 400

        student_id = data['student_id']
        response_text = data['response_text']

        # Validate input data
        if not response_text.strip():
            return jsonify({'error': 'Response text cannot be empty'}), 400

        # Store in database
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO responses (student_id, response_text) VALUES (?, ?)',
            (student_id, response_text)
        )
        conn.commit()
        conn.close()

        return jsonify({
            'message': 'Response submitted successfully',
            'timestamp': datetime.now().isoformat()
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate_summary', methods=['GET'])
def generate_summary():
    try:
        # Get time range parameters (optional)
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')

        # Fetch responses from database
        conn = get_db_connection()
        cur = conn.cursor()
        
        if start_time and end_time:
            cur.execute('''
                SELECT response_text FROM responses 
                WHERE timestamp BETWEEN ? AND ?
                ORDER BY timestamp DESC
            ''', (start_time, end_time))
        else:
            cur.execute('SELECT response_text FROM responses ORDER BY timestamp DESC')
        
        responses = cur.fetchall()
        conn.close()

        if not responses:
            return jsonify({
                'message': 'No responses found for summarization'
            }), 404

        # Combine all responses into a single text
        all_responses = "\n".join([row['response_text'] for row in responses])

        # Generate summary using Ollama
        prompt = f"Please provide a concise summary of these student responses:\n{all_responses}"
        
        try:
            response = requests.post(
                OLLAMA_API_URL,
                json={
                    "model": "mistral",  # or any other model you have pulled in Ollama
                    "prompt": prompt,
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                summary = response.json().get('response', '')
            else:
                return jsonify({
                    'error': f'Error from Ollama API: {response.text}'
                }), 500

        except Exception as e:
            return jsonify({
                'error': f'Error generating summary: {str(e)}'
            }), 500

        return jsonify({
            'summary': summary,
            'response_count': len(responses),
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

