""" This is the update function that updates the data in the database."""
import requests

from pricemap.core.config import settings
from pricemap.core.logger import logger
from pricemap.core.parsing_listing import ParsingListing
from pricemap.crud.listing import CRUDListing
from pricemap.crud.listing_history import CRUDListingHistory
from pricemap.database.session import Database


def update() -> None:
    """Update the data in the database
    We make a request to the listingapi server to get the listings.
    We get the listings and we put them in a variable called response_listings.
    We check if the HTTP code is 200. If it is, we continue the loop.
    If the HTTP code is different than 200, we break the loop.
    We generate the listings in the database.

    Returns:
        return a success message
    """
    # Looping over all places

    # init database and create listings and history_price table if not exists
    database = Database()
    database.init_listing_table()
    database.init_history_price_table()

    # Loop over all places
    for geom in settings.DISTRICT_GEOMS.values():
        page = 0

        # Looping until we have a HTTP code different than 200
        while True:
            page += 1
            url = f"http://listingapi:5000/listings/{str(geom)}?page={page}"
            # Making the request to get the listings
            response_listings = requests.get(url)

            # If the HTTP code is different than 200, we break the loop
            if response_listings.status_code == 200:
                generate_listing_in_database(
                    response_listings=response_listings.json(),
                    geom=geom,
                    database=database,
                )
            else:
                break
    return "Data updated", 200


def generate_listing_in_database(
    response_listings: dict, geom: int, database: Database
) -> None:
    """Generate listing in database
    We create a ParsingListing object with the response_listing and the geom
    We extract the values for the listing object (price_id, place_id, price, area, room_count)
    We check if listing_id is set
    If the listing is already in the database, we update it
    If not, we create it
    We create a ListingHistory object with the listing_id and the price
    We create a ListingHistory object with the listing_id and the price

    Args:
        response_listings dict: List of listings from request
        geom (int): place id
        database (Database):  Database object
    """

    for response_listing in response_listings:
        # Set all values for listing object (price_id, place_id, price, area, room_count)
        listing = ParsingListing(
            response_listing=response_listing, geom=geom
        ).extract()

        # Check if listing_id is set
        if listing.listing_id is None:
            continue

        crud_listing = CRUDListing()
        crud_listing_history = CRUDListingHistory()

        # If the listing is already in the database, we update it
        # If not, we create it
        if crud_listing.get(listing.listing_id) is None:
            logger.debug(f"Create listing for id:{listing.listing_id}")
            crud_listing.create(listing)
        else:
            logger.debug(f"Updating listing for id:{listing.listing_id}")
            crud_listing.update(listing)
        crud_listing_history.create(listing.listing_id, listing.price)
