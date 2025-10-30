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
    # Tries to get connection to the database
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
        return None 


def add_restaurant(restaurant_data):

    conn = None
    new_id = None
    
    # Organize data to use in the SQL query
    columns = ', '.join(restaurant_data.keys())
    values = tuple(restaurant_data.values())

    # Create placeholders for security
    placeholders = ', '.join(['%s'] * len(restaurant_data))
    # The RETURNING id to get the newly generated id
    query = f"INSERT INTO restaurants ({columns}) VALUES ({placeholders}) RETURNING id;"
    
    try:
        conn = get_db_connection()
        if conn is None:
            return None # Connection failure

        cursor = conn.cursor()
        
        # INSERT query with parameters
        cursor.execute(query, values)
        
        # Fetch id
        new_id = cursor.fetchone()[0]
        
        conn.commit() 
        cursor.close()
        return new_id

    except psycopg2.IntegrityError as e:
        print(f"Integrity error. {e}")
        if conn:
            conn.rollback()
        return None
        
    except Exception as e:
        print(f"INSERT error using the query {query}. {e}")
        print(f"Values = {values} and columns = {columns}")
        if conn:
            conn.rollback()
        return None
        
    finally:
        if conn:
            conn.close()



# Fetch all restaurants or restaurant by id
def fetch_restaurants_data(restaurant_id=None):
    conn = None

    data = []
    try:
        conn = get_db_connection()
        if conn is None:
            return None # Connection failure
            
        cursor = conn.cursor()

        if restaurant_id is None:
            query = "SELECT * FROM restaurants ORDER BY id;"
            parameters = None
        else:
            query = "SELECT * FROM restaurants WHERE id = %s"
            parameters = (restaurant_id,)
        
        cursor.execute(query, parameters)

        # Get column names and fetch data
        column_names = [desc[0] for desc in cursor.description]
        # Fetch data (a list of tuples)
        rows = cursor.fetchall()

        # Convert data into a list of dicts
        for row in rows:
            row_dict = dict(zip(column_names, row))
            data.append(row_dict)
        
        cursor.close()
        return data

    except Exception as e:
        print(f"An error occurred during fetch operation. {e}")
        return None
        
    finally:
        if conn:
            conn.close()


def update_restaurant(restaurant_data, restaurant_id):
    conn = None

    try:
        conn = get_db_connection()
        if conn is None:
            return None

        cursor = conn.cursor()

        values = [] # Used to get all values in order to pass as parameter
        set_clauses = []

        for key, value in restaurant_data.items():
            set_clauses.append(f"{key} = %s")
            values.append(value)

        
        final_set_clauses = ', '.join(set_clauses) # Transforms into str for the query
        values.append(restaurant_id) # Append id to pass as param

        query = f"UPDATE restaurants SET {final_set_clauses} WHERE id = %s;"
        values = tuple(values)

        cursor.execute(query, values)
            
        rows_updated = cursor.rowcount

        conn.commit()

        if rows_updated == 1:
            return True
        else:
            return False

    except Exception as e:
        print(f"An error has occured when trying to update the query. {e} ")

    finally:
        if conn:
            conn.close()