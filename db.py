import sqlite3
import os
from typing import List, Dict, Any, Optional

DB_FILE = os.path.join(os.path.dirname(__file__), "campus_compass.db")

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS floors (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        elevation REAL NOT NULL,
        height REAL NOT NULL,
        description TEXT
    );

    CREATE TABLE IF NOT EXISTS rooms (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        room_number TEXT,
        floor_id INTEGER NOT NULL,
        department TEXT NOT NULL,
        room_type TEXT NOT NULL,
        x REAL NOT NULL,
        y REAL NOT NULL,
        z REAL NOT NULL,
        door_x REAL NOT NULL,
        door_y REAL NOT NULL,
        width REAL,
        length REAL,
        area_sqm REAL,
        info TEXT,
        color TEXT DEFAULT '#3b82f6',
        FOREIGN KEY (floor_id) REFERENCES floors(id)
    );

    CREATE TABLE IF NOT EXISTS faculty (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        designation TEXT NOT NULL,
        department TEXT NOT NULL,
        cabin_room_id TEXT NOT NULL,
        cabin_name TEXT NOT NULL,
        floor_id INTEGER NOT NULL,
        subject TEXT,
        FOREIGN KEY (cabin_room_id) REFERENCES rooms(id)
    );

    CREATE TABLE IF NOT EXISTS staircases (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        stair_type TEXT NOT NULL,
        floors_connected TEXT NOT NULL,
        x REAL NOT NULL,
        y REAL NOT NULL,
        width REAL NOT NULL,
        length REAL NOT NULL
    );

    CREATE TABLE IF NOT EXISTS emergency_services (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        service_type TEXT NOT NULL,
        phone TEXT NOT NULL,
        description TEXT,
        latitude REAL,
        longitude REAL
    );
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized at:", DB_FILE)
