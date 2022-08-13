from sqlalchemy import Column, Integer


class Listing:
    __tablename__ = "listing"
    listing_id = Column(Integer, primary_key=True)
    place_id = Column(Integer)
    price = Column(Integer)
    area = Column(Integer)
    room_count = Column(Integer)
