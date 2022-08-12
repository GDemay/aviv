from sqlalchemy import Boolean, Column, Integer, String


class Apartment():
    __tablename__ = "apartment"
    listing_id = Column(Integer, primary_key=True)
    place_id = Column(Integer)
    price = Column(Integer)
    area = Column(Integer)
    room_count = Column(Integer)
