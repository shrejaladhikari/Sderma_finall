from flask import Flask, render_template, request, redirect, flash
import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = "secret"

# Dataset
data = pd.read_csv('Nepali_Derma.csv')
derma_list = data.to_dict(orient='records')

# Get database connection from environment variable
DB_CONNECTION_STRING = os.getenv('DATABASE_URL')

def init_db():
    """Initialize the PostgreSQL database and create the bookings table if it doesn't exist."""
    try:
        # Connect to PostgreSQL using the connection string
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

@app.route('/book_now', methods=['GET', 'POST'])
def book_now():
    if request.method == 'POST':
        try:
            dermatologist_id = request.form['id']
            user_name = request.form['user_name']
            user_email = request.form['user_email']
            user_contact = request.form['user_contact']
            appointment_date = request.form['appointment_date']
            appointment_time = request.form['appointment_time']

            selected_dermatologist = next((d for d in derma_list if str(d['Dermatologist ID']) == dermatologist_id), None)

            if selected_dermatologist:
                # Connect to PostgreSQL database
                conn = psycopg2.connect(DB_CONNECTION_STRING)
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO bookings (
                                    user_name, user_email, user_contact, dermatologist_name, 
                                    clinic, expertise, location, city, 
                                    appointment_date, appointment_time
                                  ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                               (user_name, user_email, user_contact,
                                selected_dermatologist['Name'], selected_dermatologist['Clinic Name'],
                                selected_dermatologist['Expertise'], selected_dermatologist['Location'],
                                selected_dermatologist['City'], appointment_date, appointment_time))
                conn.commit()
                cursor.close()
                conn.close()

            flash("Booking confirmed successfully!", "success")
        except Exception as e:
            print(f"Error occurred: {e}")
            flash("An error occurred while processing the booking.", "danger")

    return render_template('book_now.html', dermatologists=derma_list)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
