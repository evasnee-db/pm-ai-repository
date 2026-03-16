from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# Database configuration
DATABASE = 'journal.db'

def init_db():
    """Initialize the database with journal entries table"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS journal_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL UNIQUE,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

def get_entry_by_date(date):
    """Get journal entry for a specific date"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT content FROM journal_entries WHERE date = ?', (date,))
        result = cursor.fetchone()
        return result[0] if result else None

def save_entry(date, content):
    """Save or update a journal entry"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO journal_entries (date, content, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (date, content))
        conn.commit()

def get_all_entries():
    """Get all journal entries ordered by date descending"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT date, content FROM journal_entries ORDER BY date DESC')
        return cursor.fetchall()

@app.route('/')
def index():
    """Main journal entry page"""
    today = datetime.now().strftime('%Y-%m-%d')
    existing_entry = get_entry_by_date(today)
    return render_template('index.html', today=today, existing_entry=existing_entry)

@app.route('/save', methods=['POST'])
def save_journal_entry():
    """Save a journal entry"""
    data = request.get_json()
    date = data.get('date')
    content = data.get('content')
    
    if not date or not content:
        return jsonify({'success': False, 'message': 'Date and content are required'}), 400
    
    try:
        save_entry(date, content)
        return jsonify({'success': True, 'message': 'Entry saved successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/entries')
def view_entries():
    """View all journal entries"""
    entries = get_all_entries()
    return render_template('entries.html', entries=entries)

@app.route('/entry/<date>')
def view_entry(date):
    """View a specific journal entry"""
    entry = get_entry_by_date(date)
    if not entry:
        return "Entry not found", 404
    return render_template('entry.html', date=date, content=entry)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5001)





