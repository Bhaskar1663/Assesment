from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["train_booking"]
seats_collection = db["seats"]

def initialize_seats():
    if seats_collection.count_documents({}) == 0:
        for i in range(1, 81):
            seats_collection.insert_one({"seat_number": i, "booked": False})

initialize_seats()

@app.route("/")
def home():
    seats = list(seats_collection.find({}, {"_id": 0}))
    return render_template("index.html", seats=seats)

@app.route("/book", methods=["POST"])
def book_seats():
    num_seats = request.json.get("num_seats")

    if not num_seats or not isinstance(num_seats, int) or num_seats < 1 or num_seats > 7:
        return jsonify({"error": "Invalid number of seats. Must be between 1 and 7."}), 400

    available_seats = list(seats_collection.find({"booked": False}, {"_id": 0}))

    if len(available_seats) < num_seats:
        return jsonify({"error": "Not enough seats available."}), 400
    booked_seats = []
    for seat in available_seats:
        if len(booked_seats) < num_seats:
            booked_seats.append(seat["seat_number"])
            seats_collection.update_one({"seat_number": seat["seat_number"]}, {"$set": {"booked": True}})

    return jsonify({"booked_seats": booked_seats})

if __name__ == "__main__":
    app.run(debug=True)
