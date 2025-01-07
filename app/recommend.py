# app/recommend.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
file_path = 'skincare-dataset.csv'
df = pd.read_csv(file_path)

# Renaming the Rank column to Rating
df.rename(columns={'Rank': 'Rating'}, inplace=True)

df['features'] = df['Ingredients']

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['features'])

cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Function for recommendations
def recommend_cosmetics(skin_type, label_filter, rating_filter, brand_filter, price_range, ingredient_input=None, num_recommendations=10):
    recommended_products = df[df[skin_type] == 1]
    
    if label_filter != 'All':
        recommended_products = recommended_products[recommended_products['Label'] == label_filter]
    
    recommended_products = recommended_products[recommended_products['Rating'] == rating_filter]
    
    if brand_filter != 'All':
        recommended_products = recommended_products[recommended_products['Brand'] == brand_filter]
    
    recommended_products = recommended_products[
        (recommended_products['Price'] >= price_range[0]) & 
        (recommended_products['Price'] <= price_range[1])
    ]

    if ingredient_input:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(df['Ingredients'])
        input_vec = vectorizer.transform([ingredient_input])
        cosine_similarities = cosine_similarity(input_vec, tfidf_matrix).flatten()
        recommended_indices = cosine_similarities.argsort()[-num_recommendations:][::-1]
        ingredient_recommendations = df.iloc[recommended_indices]
        recommended_products = recommended_products[recommended_products.index.isin(ingredient_recommendations.index)]
    
    return recommended_products.sort_values(by=['Rating'], ascending=False).head(num_recommendations)