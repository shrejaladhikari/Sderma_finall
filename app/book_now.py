from flask import Flask, render_template, request, redirect, flash
import sqlite3
import pandas as pd

app = Flask(__name__)
app.secret_key = "secret"

# dataset
data = pd.read_csv('Nepali_Derma.csv')
derma_list = data.to_dict(orient='records')

import sqlite3

def init_db():
    """Initialize the database and create the bookings table."""
    try:
        conn = sqlite3.connect('bookings.db')  # Create or connect to the database
        cursor = conn.cursor()
        # Create the table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_name TEXT NOT NULL,
                            user_email TEXT NOT NULL,
                            user_contact TEXT NOT NULL,
                            dermatologist_name TEXT NOT NULL,
                            clinic TEXT NOT NULL,
                            expertise TEXT NOT NULL,
                            location TEXT NOT NULL,
                            city TEXT NOT NULL,
                            appointment_date TEXT NOT NULL,
                            appointment_time TEXT NOT NULL
                        )''')
        conn.commit()
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == '__main__':
    init_db()



if __name__ == '__main__':
    app.run(debug=True)
