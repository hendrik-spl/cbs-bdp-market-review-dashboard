# This file is used to store the database configuration

# Import statements
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
username = os.environ.get('DB_USERNAME')
password = os.environ.get('DB_PASSWORD')
dbname = os.environ.get('DB_NAME')
host = os.environ.get('DB_HOST')
port = os.environ.get('DB_PORT')

# Define the database URI
DATABASE_URI = f'postgresql://{username}:{password}@{host}:{port}/{dbname}'