""" This is the endpoints for ListingHistory """
import http.client
from typing import List

from flask import Blueprint, request

from pricemap.core.logger import logger
from pricemap.crud.listing_history import CRUDListingHistory
from pricemap.database.session import Database
from pricemap.schemas.listing_history import ListingHistory

listing_history_blueprint = Blueprint("listing_history_blueprint", __name__)

# Listing an listing id
@listing_history_blueprint.route("/<int:history_id>", methods=["GET"])
def get(history_id):
    """Get a Listing History from the database.

    Returns:
      ListingHistory : Return a json object with the listing history
    """
    crud_listing_history = CRUDListingHistory(database=Database())
    return crud_listing_history.get(history_id=history_id).dict()


# Create a listing history
@listing_history_blueprint.route("/", methods=["POST"])
def create() -> ListingHistory:
    """Create a Listing History in the database

    Returns:
      ListingHistory : Return a json object with the created listing history
    """

    logger.debug("Create a listing history")
    crud_listing_history = CRUDListingHistory(database=Database())

    logger.debug("Get data from request")
    data = request.get_json()

    logger.debug("Check if all fields are in data")
    # Check if all fields are in data except history_id and listing_id
    if any(field not in data for field in ["price", "date"]):
        logger.error(f"Missing fields in data: {data}")
        # raise http.client.HTTPException("Missing fields in data")
        return "Bad Request", http.client.BAD_REQUEST

    logger.debug("Create listing history")
    listing_history = ListingHistory(
        history_id=data["history_id"],
        listing_id=data["listing_id"],
        price=data["price"],
        date=data["date"],
    )

    logger.debug("Save listing history")
    listing_history = crud_listing_history.create(
        listing_history=listing_history
    )
    return listing_history.dict()
