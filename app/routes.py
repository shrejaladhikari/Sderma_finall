import pandas as pd
from flask import Blueprint, render_template, request, flash, redirect
from .recommend import recommend_cosmetics
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import os

main = Blueprint('main', __name__)

# Load environment variables from .env
load_dotenv()

# Get the database connection string from environment variables
DB_CONNECTION_STRING = os.getenv("DATABASE_URL")

# Load dataset globally
data = pd.read_csv('Nepali_Derma.csv')
derma_list = data.to_dict(orient='records')

@main.route('/')
def home():
    # Assign images dynamically based on index
    for index, derma in enumerate(derma_list[:6]):  # Limit to top 6 dermatologists
        derma['image'] = f'image{index + 1}.png'  # Assign images sequentially (e.g., image1.png, image2.png, etc.)
    return render_template('index.html', dermatologists=derma_list[:6])


# Route to article page
@main.route('/article')
def article():
    return render_template('article.html')

# Route to book now page
@main.route('/book_now')
def book_now():
    search_query = request.args.get('search', '')
    filtered_dermatologists = [
        d for d in derma_list
        if search_query.lower() in d['Name'].lower() or
           search_query.lower() in d['Expertise'].lower() or
           search_query.lower() in d['Location'].lower()
    ]
    return render_template('book_now.html', dermatologists=filtered_dermatologists, search_query=search_query)


# Route to book appointment
@main.route('/book', methods=['POST'])
def book():
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

    return redirect('/book_now')


# Route to get recommendation
@main.route('/get_recommendations', methods=['GET', 'POST'])
def get_recommendations():
    # Load unique labels and brands for the dropdowns
    file_path = 'skincare-dataset.csv'
    df = pd.read_csv(file_path)
    unique_labels = df['Label'].unique().tolist()
    unique_labels.insert(0, 'All')

    unique_brands = df['Brand'].unique().tolist()
    unique_brands.insert(0, 'All')

    recommendations = None  # Placeholder for recommendations

    if request.method == 'POST':
        # Get user input from the form
        skin_type = request.form['skin_type']
        label_filter = request.form['label_filter']
        rating_filter = tuple(map(int, request.form['rating_filter'].split(',')))
        brand_filter = request.form['brand_filter']
        price_range = tuple(map(float, request.form['price_range'].split(',')))
        ingredient_input = request.form['ingredient_input']

        # Get product recommendations
        recommendations = recommend_cosmetics(skin_type, label_filter, rating_filter, brand_filter, price_range,
                                              ingredient_input)

    # Prepare recommendations for rendering
    recommendations_html = None
    if recommendations is not None and not recommendations.empty:
        recommendations_html = recommendations[['Name', 'Label', 'Brand', 'Ingredients', 'Rating', 'Price']].to_html(
            classes='table',
            index=False  # Exclude the index column
        )
    else:
        recommendations_html = "<p>No products found based on your filters.</p>"

    # Check if the request is an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return recommendations_html

    # For normal requests, render the full page
    return render_template('get_recommendations.html',
                           labels=unique_labels,
                           brands=unique_brands,
                           recommendations_html=recommendations_html)
