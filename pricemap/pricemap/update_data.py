from flask import g, current_app
import requests
import psycopg2
from datetime import datetime
from pricemap.core.config import settings
from pricemap.database.session import Database
from pricemap.schemas.listing import Listing
from pricemap.crud.listing import CRUDListing


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
                "".join([s for s in listing["title"].split("pièces")[0] if s.isdigit()])
            )
        )
    except:
        apartment.room_count = 0

    try:
        apartment.price = int("".join([s for s in listing["price"] if s.isdigit()]))
    except:
        apartment.price = 0

    try:
        apartment.area = int(
            listing["title"].split("-")[1].replace(" ", "").replace("\u00a0m\u00b2", "")
        )
    except:
        apartment.area = 0

    apartment.seen_at = datetime.now()
    return apartment


# TODO Better HTTP error handling
def get_items_from_listingapi(listings, geom):
    # init database
    database = Database()
    database.init_database()

    # Create empty Apartment object

    for listing in listings:
        # Set all values for apartment object (price_id, place_id, price, area, room_count, seen_at)
        apartment = set_listing_values(listing, geom)

        # From CRUDApartment, we call the create function to insert the apartment object in the database
        crud_apartment = CRUDListing(database=database)
        if not crud_apartment.create(apartment=apartment):
            print("Error: apartment not created")


def update():
    # Looping over all places
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
                get_items_from_listingapi(listings=response.json(), geom=geom)
            else:
                break

