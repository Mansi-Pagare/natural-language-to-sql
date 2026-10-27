
import sqlite3

DB_NAME = "hospital.db"


def create_database():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS admissions (
                admission_id INTEGER PRIMARY KEY,
                hospital TEXT NOT NULL,
                department TEXT NOT NULL,
                patient_age INTEGER NOT NULL,
                length_of_stay INTEGER NOT NULL,
                readmitted INTEGER NOT NULL
                    CHECK (readmitted IN (0, 1))
            )
        """)

        count = conn.execute(
            "SELECT COUNT(*) FROM admissions"
        ).fetchone()[0]

        if count == 0:
            records = [
                ("City Hospital", "Cardiology", 65, 5, 1),
                ("City Hospital", "Neurology", 72, 8, 0),
                ("General Hospital", "Cardiology", 54, 3, 0),
                ("General Hospital", "Oncology", 61, 7, 1),
                ("North Medical", "Neurology", 43, 2, 0),
                ("North Medical", "Cardiology", 68, 6, 1),
                ("City Hospital", "Oncology", 49, 4, 0),
                ("General Hospital", "Neurology", 75, 9, 1),
            ]

            conn.executemany("""
                INSERT INTO admissions
                (hospital, department, patient_age,
                 length_of_stay, readmitted)
                VALUES (?, ?, ?, ?, ?)
            """, records)


if __name__ == "__main__":
    create_database()
    print("Hospital database created successfully!")
