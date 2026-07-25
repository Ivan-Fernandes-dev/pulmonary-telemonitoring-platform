import sqlite3
from pathlib import Path

DATABASE_NAME = "pulmonary_monitoring.db"

def create_database():
    database_path = Path(__file__).resolve().parent / DATABASE_NAME

    with sqlite3.connect(database_path) as connection:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                birth_date TEXT,
                gender TEXT,
                medical_record_number TEXT UNIQUE,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Measurements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                oxygen_saturation REAL NOT NULL,
                respiratory_rate INTEGER,
                heart_rate INTEGER,
                temperature REAL,
                movement TEXT,
                ambient_temperature REAL,
humidity REAL,
                       
                        measured_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES Patients (id)
            )
        """)

         

    
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS Alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                measurement_id INTEGER,
                alert_type TEXT NOT NULL,
                message TEXT NOT NULL,
                severity TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES Patients (id),
                FOREIGN KEY (measurement_id) REFERENCES Measurements (id)
            )
        """)

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

    connection.commit()

if __name__ == "__main__":
    create_database()
    with sqlite3.connect(DATABASE_NAME) as connection:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO Patients
            (id, full_name)
            VALUES (1, 'Paciente Teste')
        """)
        connection.commit()
    