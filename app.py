from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# ==== MongoDB Atlas Connection ====
# Replace the URI with your actual MongoDB Atlas connection string
client = MongoClient("mongodb+srv://Sadhana:Sadhana7@cluster.ouqj7fj.mongodb.net/")
db = client["flask"]
pets_collection = db["main"]

# Insert sample pets if the collection is empty
if pets_collection.count_documents({}) == 0:
    pets_collection.insert_many([
        {"name": "Buddy", "type": "Dog", "breed": "Golden Retriever", "age": "2 years", "status": "Available", "about": "Friendly and loves to play fetch.", "image": "https://images.unsplash.com/photo-1558788353-f76d92427f16"},
        {"name": "Mittens", "type": "Cat", "breed": "Tabby", "age": "1 year", "status": "Available", "about": "Loves naps and cuddles.", "image": "https://images.unsplash.com/photo-1592194996308-7b43878e84a6"},
        {"name": "Charlie", "type": "Dog", "breed": "Beagle", "age": "3 years", "status": "Available", "about": "Great with kids and other pets.", "image": "https://images.unsplash.com/photo-1560807707-8cc77767d783"},
        {"name": "Luna", "type": "Dog", "breed": "Pomeranian", "age": "1 year", "status": "Available", "about": "Tiny but full of energy.", "image": "https://images.unsplash.com/photo-1583337130417-3346a1afdd50"},
        {"name": "Oliver", "type": "Cat", "breed": "Siamese", "age": "4 years", "status": "Available", "about": "Talkative and affectionate.", "image": "https://images.unsplash.com/photo-1574158622682-e40e69881006"},
        {"name": "Max", "type": "Dog", "breed": "Poodle", "age": "2 years", "status": "Available", "about": "Calm and loves grooming.", "image": "https://images.unsplash.com/photo-1557976606-d068b971f2c4"},
        {"name": "Daisy", "type": "Dog", "breed": "Corgi", "age": "3 years", "status": "Available", "about": "Short legs, big heart.", "image": "https://images.unsplash.com/photo-1537151625747-768eb6cf92b6"},
        {"name": "Simba", "type": "Cat", "breed": "Persian", "age": "5 years", "status": "Available", "about": "Enjoys lounging in the sun.", "image": "https://images.unsplash.com/photo-1606214174585-7b5b37f2f1b4"},
        {"name": "Rocky", "type": "Dog", "breed": "German Shepherd", "age": "4 years", "status": "Available", "about": "Protective and loyal.", "image": "https://images.unsplash.com/photo-1619983081586-1b85c7c19e46"},
        {"name": "Bella", "type": "Cat", "breed": "Maine Coon", "age": "2 years", "status": "Available", "about": "Gentle giant with a loving nature.", "image": "https://images.unsplash.com/photo-1592194996308-7b43878e84a6"},
    ])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/preferences", methods=["GET", "POST"])
def preferences():
    if request.method == "POST":
        return redirect(url_for("browse"))
    return render_template("preferences.html")

@app.route("/browse")
def browse():
    pets = list(pets_collection.find())
    for pet in pets:
        pet["_id"] = str(pet["_id"])
    return render_template("browse.html", pets=pets)


@app.route("/adopt/<pet_id>", methods=["GET", "POST"])
def adopt(pet_id):
    pet = pets_collection.find_one({"_id": ObjectId(pet_id)})
    if not pet:
        return redirect(url_for("browse"))

    if request.method == "POST":
        pets_collection.update_one({"_id": ObjectId(pet_id)}, {"$set": {"status": "Adopted"}})
        return redirect(url_for("adoption_success", name=pet["name"]))

    return render_template("adoption_form.html", pet=pet)

@app.route("/adoption-success/<name>")
def adoption_success(name):
    return render_template("adoption_success.html", pet_name=name)

if __name__ == "__main__":
    app.run(debug=True)
