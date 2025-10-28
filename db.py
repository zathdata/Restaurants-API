import psycopg2
import os
from dotenv import load_dotenv

# Env variables
load_dotenv()

# POSTGRES DATABASE INFORMATION
HOSTNAME = os.getenv("DB_HOST")
DATABASE = os.getenv("DB_NAME")
USERNAME = os.getenv("DB_USER")
PWD = os.getenv("DB_PASSWORD")
PORT_ID = os.getenv("DB_PORT")



def get_db_connection():
    try:
        # Starts connection
        conn = psycopg2.connect(host = HOSTNAME,
                                dbname = DATABASE,
                                user = USERNAME,
                                password = PWD,
                                port = PORT_ID)
        return conn
    except psycopg2.Error as e:
        print(f"Failed to connect to the database. {e}")


def fetch_restaurants_data(restaurant_id=None):
    conn = None
    data = []
    try:
        # Get the connection to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if an ID was given as param
        if restaurant_id is None:
            query = "SELECT * FROM restaurants;"
            parameters = None
        else:
            query = "SELECT * FROM restaurants WHERE id = %s"
            parameters = (restaurant_id,)
        
        # Execute the query
        cursor.execute(query, parameters)

        # Get column names
        column_names = [desc[0] for desc in cursor.description]
        
        # Fetch data
        rows = cursor.fetchall()

        # Convert data into a list of dicts
        for row in rows:
            row_dict = dict(zip(column_names, row))
            data.append(row_dict)
        
        cursor.close()
        return data

    except Exception as e:
        print(f"An error occurred. {e}")
        return None
        
    finally:
        if conn:
            conn.close()
