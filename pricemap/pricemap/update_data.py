from datetime import datetime

import requests

from pricemap.core.config import settings
from pricemap.core.logger import logger
from pricemap.crud.listing import CRUDListing
from pricemap.crud.listing_history import CRUDListingHistory
from pricemap.database.session import Database
from pricemap.schemas.listing import Listing


def update():
    # Looping over all places

    # init database
    database = Database()
    database.init_database()
    database.init_history_price_table()

    for geom in settings.GEOMS_IDS:
        page = 0

        # Looping until we have a HTTP code different than 200
        while True:
            page += 1
            url = f"http://listingapi:5000/listings/{str(geom)}?page={page}"
            # Making the request to get the listings
            response = requests.get(url)

            # If the HTTP code is different than 200, we break the loop
            if response.status_code == 200:
                generate_listing_in_database(
                    listings=response.json(), geom=geom, database=database
                )
            else:
                break


# TODO Better HTTP error handling
def generate_listing_in_database(listings, geom: int, database: Database):

    # Create empty Apartment object

    for listing in listings:
        # Set all values for apartment object (price_id, place_id, price, area, room_count, seen_at)
        apartment = set_listing_values(listing, geom)

        # Check if listing_id is set
        if apartment.listing_id is None:
            continue

        crud_listing = CRUDListing(database=database)
        crud_listing_history = CRUDListingHistory(database=database)

        # If the apartment is already in the database, we update it
        # If not, we create it
        if crud_listing.get(apartment.listing_id) is None:
            crud_listing.create(apartment)
        else:
            crud_listing.update(apartment)
        # crud_listing_history.create(apartment.listing_id, apartment.price)


def set_listing_values(listing, geom):
    # Create empty Apartment object
    apartment = Listing()
    apartment.listing_id = listing["listing_id"]
    apartment.place_id = geom
    try:
        apartment.room_count = (
            1
            if "Studio" in listing["title"]
            else int(
                "".join(
                    [
                        s
                        for s in listing["title"].split("pièces")[0]
                        if s.isdigit()
                    ]
                )
            )
        )
    except:
        apartment.room_count = 0

    try:
        apartment.price = int(
            "".join([s for s in listing["price"] if s.isdigit()])
        )
    except:
        apartment.price = 0

    try:
        apartment.area = int(
            listing["title"]
            .split("-")[1]
            .replace(" ", "")
            .replace("\u00a0m\u00b2", "")
        )
    except:
        apartment.area = 0

    apartment.seen_at = datetime.now()
    return apartment
