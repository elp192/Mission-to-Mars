# Rendert a template, redirect to another url, create url
from flask import Flask, render_template, redirect, url_for
# Use pymongo to interact with Mongo database
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
@app.route("/")  # what to display when we're looking at the home page (route that Flask used)
def index():
   mars = mongo.db.mars.find_one() # Use Pymongo to find the mars collection in database
   return render_template("index.html", mars=mars) # Use mars collection

# Setup Scrapping route"
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars # Assign a new variable that points to Mongo database
   mars_data = scraping.scrape_all() # Create a new variable to hold the newly scraped data (referencing the scrape_all function in the scraping.py file exported from Jupyter Notebook)
   mars.update({}, mars_data, upsert=True) # Add an empty JSON object with {}, upsert=True indicates to Mongo to create a new document if one doesn't already exist
   return redirect('/', code=302) # Navigate our page back to / where we can see the updated content

if __name__ == "__main__":
   app.run()