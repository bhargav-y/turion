# Only used for local development
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
DB_NAME = os.getenv('POSTGRES_DB', 'telemetry')
DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')

if not all([DB_USER, DB_PASSWORD]):
    raise ValueError('Database credentials are not set')

def init_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS telemetry (
        id SERIAL PRIMARY KEY,
        timestamp INTEGER,
        value REAL,
        status SMALLINT
    );
    '''
    
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()
    print("Database initialized")

if __name__ == "__main__":
    init_db()