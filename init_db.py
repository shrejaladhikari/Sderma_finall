from app.db import init_db
from dotenv import load_dotenv
import os

# Load the .env file from the root directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

if __name__ == '__main__':
    init_db()
