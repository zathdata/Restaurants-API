from flask import Flask, jsonify
import db

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Restaurants API practice</h1>"


@app.route("/api/restaurants")
def restaurants():
    #Gets data from database
    data = db.fetch_restaurants_data()
    
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "Could not retrieve data."}), 500


@app.route("/api/restaurants/<id>")
def restaurants_by_id(id):
    data = db.fetch_restaurants_data(id)
    if data is None:
        return jsonify({"error": "An error occurred while fetching data."}), 500
    elif not data:
        return jsonify({"error": "Restaurant with that ID could not be found"}), 404
    else:
        return jsonify(data[0])

if __name__ == "__main__":
    app.run(debug=True)