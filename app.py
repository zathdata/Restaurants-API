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
        # Use silent get_json to avoid raising an exception on bad JSON
        restaurant_data = request.get_json(silent=True)
        if restaurant_data is None:
            return jsonify({"error": "Invalid or missing JSON in request body."}), 400
        if not restaurant_data:
            return jsonify({"error": "Data is empty"}), 400
        # Check if it has all required fields
        missing_fields = [field for field in REQUIRED_FIELDS if field not in restaurant_data]

        if missing_fields:
            return jsonify({
                "error": "Missing required fields.",
                "missing": missing_fields
            }), 400

        # Block manual id
        if 'id' in restaurant_data:
            return jsonify({
                "error": "Ids cant be manually set"
            }), 400
        
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
            return jsonify({"error": "Invalid number."}), 400


        # Call function to add the new restaurant
        new_id = db.add_restaurant(restaurant_data)

        # Check if the restaurant was added successfully
        if new_id is None:
            return jsonify({"error": "Failed to add restaurant."}), 500
        else:
            response = {
                "message": "Restaurant created successfully.",
                "id": new_id,
                "data_submitted": restaurant_data
            }
            return jsonify(response), 201
            
    else: # Get request
        # Fetch the data of all restaurants
        data = db.fetch_restaurants_data()
        if data is None:
            return jsonify({"error": "Could not retrieve the data."}), 500
        elif not data:
            return jsonify({"message": "No restaurants found."}), 200
        else:
            return jsonify(data), 200




@app.route("/api/restaurants/<id>", methods=['GET', 'PATCH', 'DELETE'])
def restaurants_by_id(id):

    if request.method == 'PATCH':
        # Use silent parsing to avoid raising
        restaurant_data = request.get_json(silent=True)
        if restaurant_data is None:
            return jsonify({"error": "Invalid or missing JSON in request body"}), 400

        if not restaurant_data:
            return jsonify({"error": "The data is empty"}), 400
        
        if 'id' in restaurant_data:
            return jsonify({
                "error": "Ids cant be manually set"
            }), 400
        
        filtered_data = {}
        # Get only fields that match the table
        for key in ALLOWED_FIELDS:
            if key in restaurant_data:
                filtered_data[key] = restaurant_data[key]

        if 'rating' in filtered_data:
            try:
                filtered_data['rating'] = float(filtered_data['rating'])
            except (ValueError, TypeError):
                return jsonify({"error": "Invalid number."}), 400

        result = db.update_restaurant(filtered_data, id)

        if result is None:
            return jsonify({"error": "An error has occurred when trying to update the data"}), 500
        
        if result is False:
            return jsonify({"message": "Restaurant not found."}), 404
        
        return jsonify({"message": "Restaurant updated successfully." }), 200


    elif request.method == 'DELETE':

        result = db.delete_restaurant(id)

        if result is None:
            return jsonify({"error": "Could not delete restaurant due to server error."}), 500
        if result:
            return jsonify({"message": "Restaurant has been deleted."}), 200
        else:
            return jsonify({"error": "Restaurant not found."}), 404

    else: # GET method

        # Fetch restaurant by id
        data = db.fetch_restaurants_data(id)
        if data is None:
            return jsonify({"error": "Could not retrieve the data."}), 500
        elif not data:
            return jsonify({"error": "Restaurant could not be found"}), 404
        else:
            return jsonify(data[0]), 200


if __name__ == "__main__":
    app.run(debug=True)
