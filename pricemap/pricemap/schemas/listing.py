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

    listing_id: Optional[int] = None  # Primary key
    place_id: Optional[int] = None  # Id of the place geom
    price: Optional[int] = None  # Price of the listing
    area: Optional[int] = None  # Area of the listing
    room_count: Optional[int] = None  # Number of rooms in the listing
    seen_at: Optional[
        datetime
    ] = None  # Date of the last update of the listing
