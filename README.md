# Restaurants API

A simple REST API built with Python, Flask, and PostgreSQL that serves data that about restaurants.

---

## Features

* **List all restaurants:** Get a complete list of all restaurants in the database.
* **Get a single restaurant:** Fetch details for a specific restaurant using its unique ID.
* **CRUD:** Handling HTTP requests GET, POST, PATCH and DELETE.

---

## Technologies Used

* **Backend:** Python 3, Flask
* **Database:** PostgreSQL
* **Python-PostgreSQL Connector:** psycopg2

---

## Setup

### Prerequisites

* Python installed
* PostgreSQL installed and running

### Installation

1.  **Clone the repository:**

2.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```
    
3.  **Set up the database:**
    * Create a PostgreSQL database named `restaurants_db`.
    * Create a table named `restaurants` with the query below.
      
    ```
    CREATE TABLE restaurants(
    	id SERIAL PRIMARY KEY,
    	name VARCHAR(50),
    	category VARCHAR(50),
    	address TEXT,
    	phone_number VARCHAR(15),
    	rating DECIMAL(2, 1)
    );
    ```

4.  **Create the environment file:**
    * Create a file named `.env` in the root of the project.
    * Add your database credentials to it:
        ```env
        DB_HOST=
        DB_NAME=
        DB_USER=
        DB_PASSWORD=
        DB_PORT=
        ```

5.  **Load the initial data:**
    * Load the data from the csv file to the database by running `load_data.py`


6.  **Run the Flask application:**
    * Run `app.py`
      
    The API will now be running at `http://127.0.0.1:5000`.

---

## API Endpoints

Here are the available endpoints.

### Get All Restaurants

Returns a JSON list of all restaurants.

* **Endpoint:** `/api/restaurants`
* **Method:** `GET`


### Get Single Restaurant by ID

Returns a single restaurant object.

* **Endpoint:** `/api/restaurants/<id>`
* **Method:** `GET`

### Add a Restaurant

Sends a POST request to add a restaurant to the database.

* **Endpoint:** `/api/restaurants`
* **Method:** `POST`

Example:
```
curl -X POST http://127.0.0.1:5000/api/restaurants \
     -H "Content-Type: application/json" \
     -d '{
         "name": "Free food",
         "category": "Japanese",
         "address": "12345 Main Street",
         "phone_number": "(11) 91234-9876",
         "rating": 4
     }'
```

### Update a Restaurant

Sends a PATCH request to update a restaurant. 

* **Endpoint:** `/api/restaurants/<id>`
* **Method:** `PATCH`

Example:
```
curl -X PATCH http://127.0.0.1:5000/api/restaurants/21 \
     -H "Content-Type: application/json" \
     -d '{
         "name": "Free food",
         "category": "Chinese",
         "address": "12345 Main Street",
         "phone_number": "(11) 91234-9876",
         "rating": 4.5
     }'
```

### Delete a Restaurant 

Sends a DELETE request to delete a restaurant. 

* **Endpoint:** `/api/restaurants/<id>`
* **Method:** `DELETE`

Example:
```
 curl -X DELETE http://127.0.0.1:5000/api/restaurants/21
```
