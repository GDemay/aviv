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
    """Update the data."""
    update()
    return "Datz gut", 200


# display the table listings
@app.route("/listings")
def listings():
    """Display the table listings."""
    cur = g.db.cursor()
    # List 20 first listings
    cur.execute("SELECT * FROM listings LIMIT 20;")
    listings = cur.fetchall()
    return listings


# Get a listing by id
@app.route("/listings/<int:listing_id>")
def get_listing(listing_id):
    """Get a listing by id."""
    cur = g.db.cursor()
    cur.execute("SELECT * FROM listings WHERE id = %s;", (listing_id,))
    listing = cur.fetchone()
    return [listing]



# Update a listing by id
@app.route("/listings/<int:listing_id>", methods=["PUT"])
def update_listing(listing_id):
    """Update a listing by id."""

    apartment = Apartment(
        listing_id=listing_id,
        place_id=1,
        price=random.randint(100, 1000),
        area=50,
        room_count=42,
    )
    crud = CRUDApartment(Database())
    crud.update(apartment, app.logger)
    return get_listing(listing_id)


# Delete listings table
@app.route("/listings", methods=["DELETE"])
def delete_listings():
    """Delete listings table."""
    cur = g.db.cursor()
    cur.execute("DROP TABLE listings;")
    return "Table listings deleted", 200

