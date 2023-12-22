from flask import Flask, request, jsonify
import pickle
from palatepicks import getNeighbors

# Load the recommender model
with open('palatepicks_model.pkl', 'rb') as f:
    itemDict = pickle.load(f)

# Create the Flask app
app = Flask(__name__)

@app.route("/")
def index():
    return {"status":"SUCCESS",
            "message":"Service is up"}, 200

@app.route("/home")
def home():
    return {"message":"Welcome Cafe Lovers!"}, 200

# Define the route to handle POST requests
@app.route('/recommend', methods=['POST'])
def recommend():
    # Get the cafe ID from the request
    cafe_id = request.json['cafe_id']

    # Get the list of recommended cafes
    neighbors = getNeighbors(cafe_id, 10)

    # Return the list of recommended cafes as JSON
    return jsonify({
        'neighbors': [
            {
                'name': itemDict[cafe_id]['name'],
                'distance': distance
            } for distance, cafe_id in neighbors
        ]
    })

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
