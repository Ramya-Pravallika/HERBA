"""
Database interface for Herba
Handles SQLite connection and queries
"""

import sqlite3
import json
import logging
from typing import List, Dict, Optional

db_path = "herba.db"

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables"""
    conn = get_db_connection()
    c = conn.cursor()
    
    # Remedies Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS remedies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symptom_type TEXT NOT NULL,
            name TEXT NOT NULL,
            rationale TEXT,
            steps_json TEXT,
            precautions_json TEXT,
            avoid_if_json TEXT,
            safe_for_pregnancy BOOLEAN,
            safe_for_breastfeeding BOOLEAN,
            safe_for_children BOOLEAN,
            min_age INTEGER
        )
    ''')
    
    # Seek Help Criteria Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS seek_help_criteria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symptom_type TEXT NOT NULL,
            criteria TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def get_remedies(symptom_type: str) -> List[Dict]:
    """Fetch remedies for a symptom type"""
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('SELECT * FROM remedies WHERE symptom_type = ?', (symptom_type,))
    rows = c.fetchall()
    
    remedies = []
    for row in rows:
        remedy = dict(row)
        # Parse JSON fields
        remedy['steps'] = json.loads(remedy['steps_json'])
        remedy['precautions'] = json.loads(remedy['precautions_json']) if remedy['precautions_json'] else []
        remedy['avoid_if'] = json.loads(remedy['avoid_if_json']) if remedy['avoid_if_json'] else []
        remedies.append(remedy)
        
    conn.close()
    return remedies

def get_seek_help(symptom_type: str) -> List[str]:
    """Fetch seek help criteria"""
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('SELECT criteria FROM seek_help_criteria WHERE symptom_type = ?', (symptom_type,))
    rows = c.fetchall()
    conn.close()
    
    return [row['criteria'] for row in rows]
