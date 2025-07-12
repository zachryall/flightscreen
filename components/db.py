import logging
import sqlite3
import os

logger = logging.getLogger(__name__)

DB_DIR = '/var/lib/flightscreen'
DB_FILE = os.path.join(DB_DIR, 'flights.db')

#TODO try catch for all statements
#TODO sort logging

def create_table():
    conn = None
    try:
        os.makedirs(DB_DIR, exist_ok=True)
        logger.info(f"Ensured database directory '{DB_DIR}' exists.")
        logger.info(f"Attempting to connect to database at: {DB_FILE}")
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        logger.info('Creating airline table')
        cursor.execute("""
            CREATE TABLE airlines (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE
            );
        """)
        logger.info('Creating plane_models table')
        cursor.execute("""
            CREATE TABLE plane_models (
                id INTEGER PRIMARY KEY,
                manufacturer TEXT,
                model TEXT,
                UNIQUE (manufacturer, model)
            );
        """)
        logger.info('Creating plane_registrations table')
        cursor.execute("""
            CREATE TABLE plane_registrations (
                tail_number TEXT PRIMARY KEY,
                model_id INTEGER,
                airline_id INTEGER,
                FOREIGN KEY (model_id) REFERENCES plane_model(id),
                FOREIGN KEY (airline_id) REFERENCES airlines(id)
            );
        """)
        logger.info('Creating airports table')
        cursor.execute("""
            CREATE TABLE airports (
                iata TEXT PRIMARY KEY,
                name TEXT,
                country TEXT
            );
        """)
        logger.info('Creating flights table')
        cursor.execute("""
            CREATE TABLE flights (
                id INTEGER PRIMARY KEY,
                date TEXT,
                flight_number TEXT,
                tail_number TEXT,
                airline_id INTEGER,
                origin TEXT, 
                destination TEXT,
                UNIQUE (date, tail_number, origin, destination),
                FOREIGN KEY (tail_number) REFERENCES plane_registration(tail_number),
                FOREIGN KEY (airline_id) REFERENCES airlines(id),
                FOREIGN KEY (origin) REFERENCES airports(iata),
                FOREIGN KEY (destination) REFERENCES airports(iata)
            );
        """)
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"SQLite error during database/table creation: {e}")
        # Re-raise the exception to indicate failure to the caller
        raise
    except OSError as e:
        logger.error(f"OS error (e.g., permissions) while creating directory or file: {e}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise
    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed.")

def insert_airport(flight_data):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO airports (iata, name, country) 
                VALUES (?, ?, ?)
            """, (
                flight_data['airport_origin_iata'],
                flight_data['airport_origin_name'],
                flight_data['airport_origin_country'],
            ))
            cursor.execute("""
                INSERT OR IGNORE INTO airports (iata, name, country) 
                VALUES (?, ?, ?)
            """, (
                flight_data['airport_destination_iata'],
                flight_data['airport_destination_name'],
                flight_data['airport_destination_country'],
            ))
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f'Error inserting new airport: {e}')

def insert_airline(flight_data):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO airlines (name) 
                VALUES (?)
            """, (
                flight_data['airline'],
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
        flight_data['plane_make'],
        flight_data['plane_model'],
    ))
    conn.commit()
    conn.close()

def insert_flight(flight_data):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM airlines
        WHERE name = ?
    """, (
        flight_data['airline'],
    ))

    airline_id = cursor.fetchone()

    cursor.execute("""
        INSERT OR IGNORE INTO flights (date, flight_number, tail_number, airline_id, origin, destination) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        flight_data['date'],
        flight_data['flight_number'],
        flight_data['tail_number'],
        airline_id[0],
        flight_data['airport_origin_iata'],
        flight_data['airport_destination_iata'],
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
        flight_data['plane_make'],
        flight_data['plane_model'],
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
        INSERT OR IGNORE INTO plane_registrations (tail_number, model_id, airline_id) 
        VALUES (?, ?, ?)
    """, (
        flight_data['tail_number'],
        model_id[0],
        airline_id[0],
    ))
    conn.commit()
    conn.close()

def get_daily_flight_count(date):
    result = 0
    with sqlite3.connect(DB_FILE) as conn:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        result = cursor.execute("""
            SELECT count(*) FROM flights
            WHERE date = ?
        """, (
            date,
        ))
        result = cursor.fetchone()[0]
    return result

