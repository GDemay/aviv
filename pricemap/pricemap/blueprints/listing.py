""" This is the endpoints for Listing"""
import logging
from datetime import datetime
from http import HTTPStatus
from typing import List

from flask import Blueprint, request

from pricemap.core.logger import logger
from pricemap.crud.listing import CRUDListing
from pricemap.crud.listing_history import CRUDListingHistory
from pricemap.database.session import Database
from pricemap.schemas.listing import Listing

listing_blueprint = Blueprint("listing_blueprint", __name__)

# Listing an listing id
@listing_blueprint.route("/<int:listing_id>", methods=["GET"])
def get_listing(listing_id):
    """Get a Listing from the database.

    Returns:
      Listing : Return a json object with the listing
    """
    crud_listing = CRUDListing(database=Database())
    return crud_listing.get(listing_id=listing_id).dict()


# Listing all listings
@listing_blueprint.route("/", methods=["GET"])
def listings() -> List[Listing]:
    """Get all listings from the database

    Returns:
        List[Listing]: List of all listings
    """
    crud_listing = CRUDListing(database=Database())
    return crud_listing.get_all()


@listing_blueprint.route("/<int:listing_id>", methods=["PUT"])
def update_listing(listing_id: int) -> Listing:
    """Update a listing in the database

    Args:
        listing_id (int): listing id

    Returns:
        _type_:  Return a json object with the updated listing
    """

    if not listing_id:
        logging.error("No listing id provided")
        return "Bad Request", HTTPStatus.BAD_REQUEST

    logger.debug("Update a listing")
    crud_listing = CRUDListing(database=Database())
    listing = crud_listing.get(listing_id=listing_id)

    if not listing:
        logging.error("Listing not found")
        return "Not Found", HTTPStatus.NOT_FOUND


    data = request.get_json()

    logger.debug(f"Data: {data}")
    if "price" in data:
        listing.price = data["price"]
        # We want to track the price history so we add a new entry in the history table
        crud_listing_history = CRUDListingHistory(database=Database())
        # listing_history = crud_listing_history.create(
        #    listing_id=listing_id, price=data["price"]
        # )
        # logger.error("Created listing history: {listing_history}")

    if "area" in data:
        listing.area = data["area"]
    if "room_count" in data:
        listing.room_count = data["room_count"]

    listing.seen_at = datetime.now()

    listing = crud_listing.update(listing=listing)
    return [listing]


# Delete a listing
@listing_blueprint.route("/<int:listing_id>", methods=["DELETE"])
def delete_listing(listing_id):
    """Delete a listing from the database."""
    crud_listing = CRUDListing(database=Database())
    return (
        ("Listing id deleted", 200)
        if crud_listing.delete(listing_id=listing_id)
        else ("Error while deleting listing", 500)
    )


# Delete listing table
@listing_blueprint.route("/", methods=["DELETE"])
def delete_listing_table():
    """Delete the listing table from the database."""
    crud_listing = CRUDListing(database=Database())
    crud_listing.delete()
    return "Deleted table"
