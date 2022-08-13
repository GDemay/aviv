from flask import Flask, g, render_template
import psycopg2
import requests
from pricemap.blueprints.api import api
from pricemap.blueprints.listing import listing_blueprint
import re
import random
from pricemap.core import listing
from pricemap.update_data import update
import logging
from pricemap.database.session import Database
from pricemap.schemas.listing import Listing
from pricemap.crud.listing import CRUDListing
from datetime import datetime, timedelta
from random import randrange

app = Flask(__name__)
app.config.from_object("settings")
app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(listing_blueprint, url_prefix="/listing")


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
    return "", 200

