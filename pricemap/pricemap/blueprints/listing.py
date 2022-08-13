from typing import List

from flask import Blueprint, request

from pricemap.core.logger import logger
from pricemap.crud.listing import CRUDListing
from pricemap.database.session import Database
from pricemap.schemas.listing import Listing

listing_blueprint = Blueprint("listing_blueprint", __name__)

# Listing an listing id
@listing_blueprint.route("/<int:listing_id>", methods=["GET"])
def get_listing(listing_id):
    """Get a listing from the database."""
    crud_apartment = CRUDListing(database=Database())
    return crud_apartment.get(listing_id=listing_id).dict()


# Listing all listings
@listing_blueprint.route("/", methods=["GET"])
def listings() -> List[Listing]:
    """Get all listings from the database

    Returns:
        List[Listing]: List of all listings
    """
    crud_apartment = CRUDListing(database=Database())
    return crud_apartment.get_all()


@listing_blueprint.route("/<int:listing_id>", methods=["PUT"])
def update_listing(listing_id: int) -> Listing:
    """Update a listing in the database

    Args:
        listing_id (int): listing id

    Returns:
        _type_:  Return a json object with the updated listing
    """
    crud_apartment = CRUDListing(database=Database())
    listing = crud_apartment.get(listing_id=listing_id)

    logger.debug(f"Update listing for listing_id: {listing_id}")

    data = request.get_json()

    logger.debug(f"Data: {data}")
    if "price" in data:
        listing.price = data["price"]
    if "area" in data:
        listing.area = data["area"]
    if "room_count" in data:
        listing.room_count = data["room_count"]
    if "seen_at" in data:
        listing.seen_at = data["seen_at"]

    listing = crud_apartment.update(listing=listing)
    return listing.dict()


# Delete a listing
@listing_blueprint.route("/<int:listing_id>", methods=["DELETE"])
def delete_listing(listing_id):
    """Delete a listing from the database."""
    crud_apartment = CRUDListing(database=Database())
    return (
        ("Listing id deleted", 200)
        if crud_apartment.delete(listing_id=listing_id)
        else ("Error while deleting listing", 500)
    )


# Delete listing table
@listing_blueprint.route("/", methods=["DELETE"])
def delete_listing_table():
    """Delete the listing table from the database."""
    crud_apartment = CRUDListing(database=Database())
    crud_apartment.delete()
    return "Deleted table"


# test logger
@listing_blueprint.route("/logger", methods=["GET"])
def logger_test():

    logger.error("test info")
    return "test logger"
