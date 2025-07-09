import logging
import sqlite3

logger = logging.getLogger(__name__)

DB_FILE = 'flights.db'

def create_table():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        PRAGMA foreign_keys = ON;

        CREATE TABLE airlines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        );

        CREATE TABLE plane_models (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            manufacturer TEXT,
            model TEXT,
            UNIQUE (manufacturer, model)
        );

        CREATE TABLE plane_registrations (
            tail_number TEXT PRIMARY KEY,
            model_id INTEGER,
            airline_id INTEGER,
            FOREIGN KEY (model_id) REFERENCES plane_model(id),
            FOREIGN KEY (airline_id) REFERENCES airlines(id)
        );

        CREATE TABLE airports (
            iata TEXT PRIMARY KEY,
            name TEXT,
            country TEXT
        );

        CREATE TABLE flights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            flight_number TEXT,
            tail_number TEXT,
            airline_id INTEGER,
            origin TEXT, 
            destination TEXT,
            UNIQUE (date, flight_number),
            FOREIGN KEY (tail_number) REFERENCES plane_registration(tail_number),
            FOREIGN KEY (airline_id) REFERENCES airlines(id),
            FOREIGN KEY (origin) REFERENCES airports(iata),
            FOREIGN KEY (destination) REFERENCES airports(iata)
        );
    """)
    conn.commit()
    conn.close()

def insert_airport(flight_data):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO airports (iata, name, country) 
                VALUES (?, ?, ?)
            """, (
                flight_data['iata'],
                flight_data['name'],
                flight_data['country'],
            ))
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f'Error inserting new airport: {e}')

def insert_airline(flight_data):
    with sqlite3.connect(DB_FILE) as conn
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    try:
        cursor.execute("""
            INSERT OR IGNORE INTO airlines (name) 
            VALUES (?)
        """, (
            flight_data['name'],
        ))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f'Error inserting new airport: {e}')

def insert_plane_model(flight_data):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO plane_models (manufacturer, model) 
        VALUES (?, ?)
    """, (
        flight_data['manufacturer'],
        flight_data['model'],
    ))
    conn.commit()
    conn.close()

def insert_flight(flight_data):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT airline_id FROM airlines
        WHERE name = ?
    """, (
        flight_data['airline'],
    ))

    airline_id = cursor.fetchone()

    cursor.execute("""
        INSERT INTO flights (date, flight_number, tail_number, airline_id, origin, destination) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        flight_data['date'],
        flight_data['flight_number'],
        flight_data['tail_number'],
        airline_id[0],
        flight_data['origin'],
        flight_data['destination'],
    ))
    conn.commit()
    conn.close()

def insert_plane_registration(flight_data):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM plane_models
        WHERE manufacturer = ?
        AND model = ?
    """, (
        flight_data['manufacturer'],
        flight_data['model'],
    ))

    model_id = cursor.fetchone()

    cursor.execute("""
        SELECT id FROM airlines
        WHERE name = ?
    """, (
        flight_data['airline'],
    ))

    airline_id = cursor.fetchone()

    cursor.execute("""
        INSERT INTO plane_registrations (tail_number, model_id, airline_id) 
        VALUES (?, ?, ?)
    """, (
        flight_data['tail_number'],
        model_id[0],
        airline_id[0]',
    ))
    conn.commit()
    conn.close()
