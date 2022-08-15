"""This is the base Pydantic model for a Listing"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class Listing(BaseModel):
    """This is the base model for a History

    Args:
        BaseModel is the base class for all models
    """

    listing_id: int = None  # Primary key
    place_id: int = None  # Id of the place geom
    price: int = None  # Price of the listing
    area: int = None  # Area of the listing
    room_count: int = None  # Number of rooms in the listing
    creation_date: datetime = None  # Date of creation of the listing
    deleted_at: datetime = None  # Date of deletion of the listing
