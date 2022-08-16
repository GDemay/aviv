""" This is Parse Listing function that parses the data from the API and insert it in the database."""
import logging

from pricemap.schemas.listing import Listing


class ParsingListing:
    """ This class is used for parsing the listing object from the API response"""
    def __init__(self, response_listing: dict, geom: int):
        self.response_listing = response_listing
        self.listing = Listing()
        self.geom = geom

    def get_listing_id(self) -> int:
        """Get the listing id from the listing response

        Returns:
            int: the listing id
        """
        return self.response_listing["listing_id"]

    def get_place_id(self) -> int:
        """Get the place id from the listing response

        Returns:
            int: the place id
        """
        return self.geom

    def get_room_count(self) -> int:
        """Get room count from listing response

        Returns:
            int: The number of rooms
        """

        room_count = 0
        try:
            room_count = (
                1
                if "Studio" in self.response_listing["title"]
                else int(
                    "".join(
                        [
                            s
                            for s in self.response_listing["title"].split(
                                "pièces"
                            )[0]
                            if s.isdigit()
                        ]
                    )
                )
            )
        except Exception as e:
            logging.error("Error while getting room: ", e)
        return room_count

    def get_price(self) -> int:
        """Get price from listing response

        Returns:
            int: The price of the listing
        """
        price = 0
        try:
            price = int(
                "".join(
                    [s for s in self.response_listing["price"] if s.isdigit()]
                )
            )
        except Exception as e:
            logging.error("Error while getting price: ", e)

        return price

    def get_area(self) -> int:
        """Get area from listing response

        Returns:
            int:  The area of the listing response
        """
        area = 0
        try:
            area = int(
                self.response_listing["title"]
                .split("-")[1]
                .replace(" ", "")
                .replace("\u00a0m\u00b2", "")
            )

        except Exception as e:
            logging.error("Error while getting area: ", e)
        return area

    def extract(self) -> Listing:
        """This functions will extract the values from the listing object
        Returns:
            Listing: Create from all the extracts functions a Listing object
        """
        # Create a listing object
        listing = Listing()
        # Set the listing id
        listing.listing_id = self.get_listing_id()
        # Set the place id
        listing.place_id = self.get_place_id()
        # Set the room count
        listing.room_count = self.get_room_count()
        # Set the price
        listing.price = self.get_price()
        # Set the area
        listing.area = self.get_area()

        return listing
