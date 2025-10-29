from flask import Flask, jsonify, request
import db


app = Flask(__name__)

# Required columns for POST requests
REQUIRED_FIELDS = ['name', 'category', 'address', 'phone_number', 'rating']


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
            }), 400

        # Block manual id
        if 'id' in restaurant_data:
            return jsonify({
                "error": "Ids cant be manually set"
            }), 400
        
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


@app.route("/api/restaurants/<id>")
def restaurants_by_id(id):
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
