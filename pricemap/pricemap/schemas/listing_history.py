"""This is the base Pydantic model for a ListingHistory"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ListingHistory(BaseModel):
    """This is the base model for a ListingHistory

    Args:
        BaseModel is the base class for all models
    """

    history_id: Optional[int] = None
    listing_id: Optional[
        int
    ] = None  # Foreign key linked to listing_id in Listing
    price: Optional[int] = None
    date: Optional[datetime] = None
