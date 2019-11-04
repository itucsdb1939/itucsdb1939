import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    #Seda Sügür
    """
    CREATE TABLE IF NOT EXISTS nurse(
        tc BIGINT NOT NULL PRIMARY KEY UNIQUE,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        gender VARCHAR(1) NOT NULL,
        email TEXT,
        phone BIGINT,
        dep TEXT NOT NULL,
        pass TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS prescription(
        id BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
        patient_id BIGINT REFERENCES person(tc) ON DELETE RESTRICT ON UPDATE CASCADE,
        doctor_id BIGINT REFERENCES doctor(tc) ON DELETE RESTRICT ON UPDATE CASCADE,
        type TEXT NOT NULL,
        date_start TEXT NOT NULL,
        date_end TEXT NOT NULL,
        pills TEXT NOT NULL,
        diagnosis TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS test(
        id BIGSERIAL PRIMARY KEY NOT NULL,
        patient_id BIGINT REFERENCES person(tc) ON DELETE RESTRICT ON UPDATE CASCADE,
        doctor_id BIGINT REFERENCES doctor(tc) ON DELETE RESTRICT ON UPDATE CASCADE,
        liver_func TEXT,
        thyroid_func TEXT,
        genetic TEXT,
        electrolyte TEXT,
        coagulation TEXT,
        blood_gas TEXT,
        blood_glucose TEXT,
        blood_culture TEXT,
        full_blood_count TEXT
    )
    """,
    #Buket Akgün
    """
    CREATE TABLE IF NOT EXISTS person(
        tc BIGINT NOT NULL PRIMARY KEY UNIQUE,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        gender VARCHAR(1) NOT NULL,
        email TEXT,
        phone BIGINT,
        pass TEXT NOT NULL
    )
    """,
    """ 
    CREATE TABLE IF NOT EXISTS doctor(
        tc BIGINT NOT NULL PRIMARY KEY UNIQUE,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        gender VARCHAR(1) NOT NULL,
        email TEXT,
        phone BIGINT,
        room INTEGER NOT NULL,
        dep TEXT NOT NULL,
        pass TEXT NOT NULL 
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS surgery(
        id BIGINT PRIMARY KEY NOT NULL,
        patient_id BIGINT REFERENCES person(tc) ON DELETE RESTRICT ON UPDATE CASCADE,
        doctor_id BIGINT REFERENCES doctor(tc) ON DELETE RESTRICT ON UPDATE CASCADE,
        nurse_id BIGINT REFERENCES nurse(tc) ON DELETE RESTRICT ON UPDATE CASCADE,
        op_room INTEGER NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        blood_type TEXT NOT NULL,
        op_report TEXT,
        UNIQUE(date,time,op_room)
    )
    """,
    #Extras
    """
    CREATE TABLE IF NOT EXISTS record(
        patient_id BIGINT REFERENCES person(tc) ON DELETE RESTRICT ON UPDATE CASCADE,
        doctor_id BIGINT REFERENCES doctor(tc) ON DELETE RESTRICT ON UPDATE CASCADE,
        pres_id BIGINT REFERENCES prescription(id) ON DELETE RESTRICT ON UPDATE CASCADE,
        diagnosis TEXT,
        test_id BIGINT REFERENCES test(id) ON DELETE RESTRICT ON UPDATE CASCADE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS all_appoinments(
        doctor_id BIGINT REFERENCES doctor(tc) ON DELETE RESTRICT ON UPDATE CASCADE,
        date TEXT NOT NULL,
        time TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS taken_appoinments(
        patient_id BIGINT REFERENCES person(tc) ON DELETE RESTRICT ON UPDATE CASCADE,
        doctor_id BIGINT REFERENCES doctor(tc) ON DELETE RESTRICT ON UPDATE CASCADE,
        date TEXT NOT NULL,
        time TEXT NOT NULL
    )
    """
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
