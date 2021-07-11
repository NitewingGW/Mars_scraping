from flask import *
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

from pymongo import *
import scraping
import numpy as np


app = Flask(__name__)
# Use flask_pymongo to set up mongo connection
# URI uniform resource identifier similar to a URL
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
   mars = mongo.db.mars.find_one() # uses PyMongo to find the "mars" collection in our database, 
                                # which we will create when we convert our Jupyter scraping code
                                # to Python Script
   return render_template("index.html", mars=mars)
            # tells Flask to return an HTML template using an index.html file
            # mars=mars tells Python to use the "mars" collection in MongoDB
            # This function is what links our visual representation of our work, 
            # our web app, to the code that powers it
            
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True) #We're inserting data, so first we'll need to add an 
                        #empty JSON object with {} in place of the query_parameter. Next, we'll 
                        #use the data we have stored in mars_data. Finally, the option we'll 
                        #include is upsert=True. This indicates to Mongo to create a new document 
                        #if one doesn't already exist, and new data will always be saved (even if we 
                        #haven't already created a document for it).
   return redirect('/', code=302) # we will add a redirect after successfully scraping the data:
                        # return redirect('/', code=302). This will navigate our page back to / 
                        # where we can see the updated content
    

if __name__ == "__main__":
   app.run()