from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

OLLAMA_API_URL = "http://host.docker.internal:11434/api/generate"

# Database initialization
def init_db():
    conn = sqlite3.connect('data/responses.db')
    c = conn.cursor()
    
    # Create responses table
    c.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            response_text TEXT NOT NULL,
            question_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (question_id) REFERENCES questions (id)
        )
    ''')
    
    # Create questions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database when the application starts
init_db()

def get_db_connection():
    conn = sqlite3.connect('data/responses.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/submit_question', methods=['POST'])
def submit_question():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'question_text' not in data:
            return jsonify({
                'error': 'Missing required field: question_text'
            }), 400

        question_text = data['question_text']

        # Validate input data
        if not question_text.strip():
            return jsonify({'error': 'Question text cannot be empty'}), 400

        # Store in database
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO questions (question_text) VALUES (?)',
            (question_text,)
        )
        question_id = cur.lastrowid
        conn.commit()
        conn.close()

        return jsonify({
            'message': 'Question submitted successfully',
            'question_id': question_id,
            'timestamp': datetime.now().isoformat()
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_question', methods=['GET'])
def get_question():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get the most recent question
        cur.execute('''
            SELECT id, question_text, timestamp 
            FROM questions 
            ORDER BY timestamp DESC 
            LIMIT 1
        ''')
        
        question = cur.fetchone()
        conn.close()

        if not question:
            return jsonify({
                'message': 'No questions found'
            }), 404

        return jsonify({
            'question_id': question['id'],
            'question_text': question['question_text'],
            'timestamp': question['timestamp']
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Your existing submit_response function, updated to include question_id
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
        question_id = data.get('question_id')  # Optional, but recommended

        # Validate input data
        if not response_text.strip():
            return jsonify({'error': 'Response text cannot be empty'}), 400

        # Store in database
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO responses (student_id, response_text, question_id) VALUES (?, ?, ?)',
            (student_id, response_text, question_id)
        )
        conn.commit()
        conn.close()

        return jsonify({
            'message': 'Response submitted successfully',
            'timestamp': datetime.now().isoformat()
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update generate_summary to optionally filter by question_id
@app.route('/generate_summary', methods=['GET'])
def generate_summary():
    try:
        # Get parameters
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        question_id = request.args.get('question_id')

        # Fetch responses from database
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = 'SELECT response_text FROM responses'
        params = []
        conditions = []

        if start_time and end_time:
            conditions.append('timestamp BETWEEN ? AND ?')
            params.extend([start_time, end_time])

        if question_id:
            conditions.append('question_id = ?')
            params.append(question_id)

        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)

        query += ' ORDER BY timestamp DESC'
        
        cur.execute(query, params)
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
                    "model": "llama3.1:latest",
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
