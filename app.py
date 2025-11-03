from flask import Flask, jsonify, request
import db


app = Flask(__name__)

# Required columns for POST requests
# REQUIRED_FIELDS = ['name', 'category', 'address', 'phone_number', 'rating']
REQUIRED_FIELDS = {'name', 'category', 'address', 'phone_number', 'rating'}
ALLOWED_FIELDS = REQUIRED_FIELDS


@app.route("/")
def home():
    return "<h1>Restaurants API practice</h1>"


@app.route("/api/restaurants", methods=['GET', 'POST'])
def restaurants():
    if request.method == 'POST':
        # Add new restaurant
        
        try:
            restaurant_data = request.get_json()
        except Exception:
            return jsonify({"error": "Invalid JSON format in request body."})

        if not restaurant_data:
            return jsonify({"error": "Data is empty"})
        # Check if it has all required fields
        missing_fields = [field for field in REQUIRED_FIELDS if field not in restaurant_data]

        if missing_fields:
            return jsonify({
                "error": "Missing required fields.",
                "missing": missing_fields
            })

        # Block manual id
        if 'id' in restaurant_data:
            return jsonify({
                "error": "Ids cant be manually set"
            })
        
        filtered_data = {}
        # Exclude extra fields
        for key in ALLOWED_FIELDS:
            if key in restaurant_data:
                filtered_data[key] = restaurant_data[key]

        restaurant_data = filtered_data
        
        # Convert rating to float
        try:
            restaurant_data['rating'] = float(restaurant_data['rating'])
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid number."})


        # Call function to add the new restaurant
        new_id = db.add_restaurant(restaurant_data)

        # Check if the restaurant was added successfully
        if new_id is None:
            return jsonify({"error": "Failed to add restaurant."})
        else:
            response = {
                "message": "Restaurant created successfully.",
                "id": new_id,
                "data_submitted": restaurant_data
            }
            return jsonify(response)
            
    else: # Get request
        # Fetch the data of all restaurants
        data = db.fetch_restaurants_data()
        
        if data is None:
             return jsonify({"error": "Could not retrieve the data."})
        elif not data:
            return jsonify({"message": "No restaurants found."})
        else:
            return jsonify(data)




@app.route("/api/restaurants/<id>", methods=['GET', 'PATCH', 'DELETE'])
def restaurants_by_id(id):

    if request.method == 'PATCH':
        try:
            restaurant_data = request.get_json()
        except Exception:
            return jsonify({"error": "Invalid JSON format in request body"})

        if not restaurant_data:
            return jsonify({"error": "The data is empty"})
        
        if 'id' in restaurant_data:
            return jsonify({
                "error": "Ids cant be manually set"
            })
        
        filtered_data = {}
        # Get only fields that match the table
        for key in ALLOWED_FIELDS:
            if key in restaurant_data:
                filtered_data[key] = restaurant_data[key]

        if 'rating' in filtered_data:
            try:
                restaurant_data['rating'] = float(restaurant_data['rating'])
            except (ValueError, TypeError):
                return jsonify({"error": "Invalid number."})
        

        result = db.update_restaurant(restaurant_data, id)

        if result is None:
            return jsonify({"error": "An error has occurred when trying to update the data"})
        
        if result is False:
            return jsonify({"message": "Restaurant not found."})
        
        return jsonify({"message": "Restaurant updated successfully." })


    elif request.method == 'DELETE':

        result = db.delete_restaurant(id)

        if result:
            return jsonify({"message": "Restaurant has been deleted."})
        else:
            return jsonify({"error": "Restaurant not found."})

    else: # GET method

        # Fetch restaurant by id
        data = db.fetch_restaurants_data(id)
        if data is None:
            return jsonify({"error": "Could not retrieve the data."})
        elif not data:
            return jsonify({"error": "Restaurant could not be found"})
        else:
            return jsonify(data[0])


if __name__ == "__main__":
    app.run(debug=True)
