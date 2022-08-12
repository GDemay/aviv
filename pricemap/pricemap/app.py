from flask import Flask, g, render_template
import psycopg2
import requests
from pricemap.blueprints.api import api
import re
import random
from pricemap.core import apartment
from pricemap.update_data import update
from pricemap.core.apartment import set_listings_db
import logging
from pricemap.database.session import Database
from pricemap.schemas.apartment import Apartment
from pricemap.crud.apartment import CRUDApartment
from datetime import datetime, timedelta
from random import randrange

app = Flask(__name__)
app.config.from_object("settings")
app.register_blueprint(api, url_prefix="/api")


@app.before_request
def before_request():
    """Before every requests, connect to database in case of any disconnection."""
    if not hasattr(app, "_request_counter"):
        app._request_counter = 0
    if not hasattr(app, "db") or app.db.closed or app._request_counter == 10000:
        if hasattr(app, "db"):
            app.db.close()
        app.db = psycopg2.connect(**app.config["DATABASE"])
        app._request_counter = 0
    app._request_counter += 1
    g.db = app.db


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/update_data")
def update_data():
   '''Update the data.'''
   update()
   return "", 200
 
# Listing an listing id
@app.route("/listings/<int:listing_id>", methods=["GET"])
def listing(listing_id):
    """Get a listing from the database."""
    database = Database()
    crud_apartment = CRUDApartment(database=database)
    listing = crud_apartment.get(listing_id=listing_id)
    return listing
  
# Listing all listings
@app.route("/listings")
def listings():
    """Get all listings from the database."""
    database = Database()
    crud_apartment = CRUDApartment(database=database)
    listings = crud_apartment.get_all()
    return listings

# Update a listing
@app.route("/listings/<int:listing_id>", methods=["PUT"])
def update_listing(listing_id):
    """Update a listing from the database."""
    database = Database()
    crud_apartment = CRUDApartment(database=database)
    listing = crud_apartment.get(listing_id=listing_id)
    listing.price = 1000
    crud_apartment.update(apartment=listing)
    return listing

# Delete a listing
@app.route("/listings/<int:listing_id>", methods=["DELETE"])
def delete_listing(listing_id):
    """Delete a listing from the database."""
    database = Database()
    crud_apartment = CRUDApartment(database=database)
    listing = crud_apartment.get(listing_id=listing_id)
    crud_apartment.delete(apartment=listing)
    return listing

# Delete listing table
@app.route("/listings", methods=["DELETE"])
def delete_listing_table():
    """Delete the listing table from the database."""
    database = Database()
    crud_apartment = CRUDApartment(database=database)
    crud_apartment.delete_table()
    return "Deleted table"