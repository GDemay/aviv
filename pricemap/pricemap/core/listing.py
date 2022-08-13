import re, requests
import logging
from pricemap.models.listing import Listing
from pricemap.crud.listing import CRUDListing

# Create an appartment object from listing
def create_listing(listing, place_id: int):
    return Listing(
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

