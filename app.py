# Rendert a template, redirect to another url, create url
from flask import Flask, render_template, redirect, url_for
# use pymongo to interact with Mongo database
from flask_pymongo import PyMongo
# Convert from Jupyter Notebook to Python
import scraping

# Set up Flask
app = Flask(__name__)

# Python connect to Mongo using PyMongo
# Use flask_pymongo to set up mongo connection
# Left: App will connect to Mongo using a URI, rigth: URI we'll be using to connect our app to Mongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Define route for the HTML page
@app.route("/")  # what to display when we're looking at the home page
def index():
   mars = mongo.db.mars.find_one() # Use Pymongo to find the mars collection in database
   return render_template("index.html", mars=mars) # Use mars collection


