from pricemap.database.session import Database
from pricemap.database.session import Database
from pricemap.schemas.listing import Listing
from pricemap.crud.listing import CRUDListing
from flask import Blueprint, jsonify, g

listing_blueprint = Blueprint("listing_blueprint", __name__)

# Listing an listing id
@listing_blueprint.route("/<int:listing_id>", methods=["GET"])
def get_listing(listing_id):
    """Get a listing from the database."""
    database = Database()
    crud_apartment = CRUDListing(database=database)
    listing = crud_apartment.get(listing_id=listing_id)
    return listing


# Listing all listings
@listing_blueprint.route("/", methods=["GET"])
def listings():
    """Get all listings from the database."""
    database = Database()
    crud_apartment = CRUDListing(database=database)
    listings = crud_apartment.get_all()
    return listings


# Update a listing
@listing_blueprint.route("/<int:listing_id>", methods=["PUT"])
def update_listing(listing_id):
    """Update a listing from the database."""
    database = Database()
    crud_apartment = CRUDListing(database=database)
    listing = crud_apartment.get(listing_id=listing_id)
    listing["price"] = 1000
    crud_apartment.update(apartment=listing)
    return listing


# Delete a listing
@listing_blueprint.route("/<int:listing_id>", methods=["DELETE"])
def delete_listing(listing_id):
    """Delete a listing from the database."""
    database = Database()
    crud_apartment = CRUDListing(database=database)
    listing = crud_apartment.get(listing_id=listing_id)
    crud_apartment.delete(apartment=listing)
    return listing


# Delete listing table
@listing_blueprint.route("/", methods=["DELETE"])
def delete_listing_table():
    """Delete the listing table from the database."""
    database = Database()
    crud_apartment = CRUDListing(database=database)
    crud_apartment.delete()
    return "Deleted table"
