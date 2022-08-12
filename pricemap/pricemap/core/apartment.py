import re, requests
import logging
from pricemap.models.apartment import Apartment
from pricemap.crud.apartment import CRUDApartment

def set_listings_db(place_id):

    return listings


# Create an appartment object from listing
def create_appartment(listing, place_id: int):
    return Apartment(
        listing_id=listing["listing_id"],
        place_id=place_id,
        price=set_price(listing["price"]),
        area=set_area(listing["title"]),
        room_count=42,
    )


def set_area(title):
    try:
        return int(title.split(" - ")[1].split("m²")[0])
    except IndexError:
        return None


def set_price(price):
    # Remove all non digit characters
    try:
        return int(re.sub("[^0-9]", "", price))
    except ValueError:
        return None

