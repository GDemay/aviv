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
def get_listing(listing_id: int) -> Listing:
    """Get a Listing from the database.

    Returns:
      Listing : Return a json object with the listing
    """
    crud_listing = CRUDListing()
    return crud_listing.get(listing_id=listing_id).dict()


# Listing all listings
@listing_blueprint.route("/", methods=["GET"])
def listings() -> List[Listing]:
    """Get all listings from the database

    Returns:
        List[Listing]: List of all listings
    """
    crud_listing = CRUDListing()
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
    crud_listing = CRUDListing()
    listing = crud_listing.get(listing_id=listing_id)

    if not listing:
        logging.error("Listing not found")
        return "Not Found", HTTPStatus.NOT_FOUND

    data = request.get_json()

    logger.debug(f"Data: {data}")
    if "price" in data:
        listing.price = data["price"]
        # We want to track the price history so we add a new entry in the history table
        crud_listing_history = CRUDListingHistory()
        if listing_history := crud_listing_history.create(
            listing_id=listing_id, price=data["price"]
        ):
            logger.debug(f"Listing history: {listing_history.dict()}")
        else:
            logger.error("Could not create listing history")

    if "area" in data:
        listing.area = data["area"]
    if "room_count" in data:
        listing.room_count = data["room_count"]

    listing = crud_listing.update(listing=listing)
    return listing.dict()


# Delete a listing
@listing_blueprint.route("/<int:listing_id>", methods=["DELETE"])
def delete_listing(listing_id: int) -> Listing:
    """Delete a listing from the database.
    params: listing_id (int): listing id
    """
    crud_listing = CRUDListing()
    return (
        ("Listing id deleted", 200)
        if crud_listing.delete(listing_id=listing_id)
        else ("Error while deleting listing", 500)
    )


# Delete listing table
@listing_blueprint.route("/", methods=["DELETE"])
def delete_listing_table() -> str:
    """Delete the listing table from the database."""
    crud_listing = CRUDListing()
    crud_listing.delete()
    return "Deleted table"


# Drop table listing
@listing_blueprint.route("/drop", methods=["DELETE"])
def drop_listing_table() -> str:
    """Drop the listing table from the database."""
    db = Database()
    return db.delete_table()


# Get the average price by m² for a given place_id
@listing_blueprint.route("/average/<int:place_id>", methods=["GET"])
def get_average_price_by_place_id(place_id: int) -> Listing:
    """Get the average price by m² for a given place_id.
    params: place_id (int): place id
    """
    crud_listing = CRUDListing()
    return crud_listing.get_average_price_by_place_id(place_id=place_id)
