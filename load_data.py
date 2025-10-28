import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load env variables
load_dotenv()

# POSTGRES DATABASE INFORMATION

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")

# Fix password symbols issues to the database URL
encoded_password = quote_plus(password)

try:
    # Read the CSV file into a DataFrame
    df = pd.read_csv('restaurants.csv', encoding='utf-8')

except FileNotFoundError:
    print(f"Error: CSV file not found at current path")
    exit()
except Exception as e:
    print(f"An error occurred loading the file. {e}")
    exit()



DATABASE_URL = f"postgresql+psycopg2://{user}:{encoded_password}@{host}:{port}/{database}"
engine = None

TABLE_NAME = "restaurants"



try:
    engine = create_engine(DATABASE_URL)

    # Insert data into the table
    df.to_sql(
        TABLE_NAME, 
        engine, 
        if_exists='append',
        index=False,
        chunksize=500
    )
    

except Exception as e:
    print(f"Error when inserting the data. {e}")

finally:
    # Close engine
    if engine:
        engine.dispose()

