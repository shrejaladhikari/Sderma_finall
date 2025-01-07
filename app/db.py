import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database connection settings (from environment variables)
DB_CONNECTION_STRING = os.getenv("DATABASE_URL")

def init_db():
    """Initialize the PostgreSQL database and create the bookings table if it doesn't exist."""
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = conn.cursor()

        # Create the bookings table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id SERIAL PRIMARY KEY,
                user_name TEXT NOT NULL,
                user_email TEXT NOT NULL,
                user_contact TEXT NOT NULL,
                dermatologist_name TEXT NOT NULL,
                clinic TEXT NOT NULL,
                expertise TEXT NOT NULL,
                location TEXT NOT NULL,
                city TEXT NOT NULL,
                appointment_date DATE NOT NULL,
                appointment_time TIME NOT NULL
            );
        ''')

        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")

def execute_query(query, values=None):
    """
    Execute a given SQL query with optional parameter values.
    Args:
        query (str): The SQL query to execute.
        values (tuple): Optional parameter values for the query.

    Returns:
        list: Query results, if applicable.
    """
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = conn.cursor()

        # Execute the query
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)

        # Fetch results if it's a SELECT query
        if query.strip().lower().startswith("select"):
            results = cursor.fetchall()
        else:
            results = None
            conn.commit()

        cursor.close()
        conn.close()
        return results
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
