""" This is the CRUD for Listing (create, read, update, delete) """
from pricemap.core.logger import logger
from pricemap.schemas.listing import Listing


class CRUDListing:
    def __init__(self, database):
        self.database = database

    def get(self, listing_id: int) -> Listing:
        """Get a listing from id

        Args:
            listing_id (int):  listing id

        Returns:
            _type_:  Listing
        """
        # TODO Ca semble casser quelque chose, à voir
        #  if not isinstance(listing_id, int):
        #      return None
        sql = """
      SELECT * FROM listings WHERE id = %s
      """
        try:
            self.database.db_cursor.execute(sql, (listing_id,))
            listing = self.database.db_cursor.fetchone()

            if listing is None:
                logger.debug("Listing not found")
                return None

            return Listing(
                listing_id=listing[0],
                place_id=listing[1],
                price=listing[2],
                area=listing[3],
                room_count=listing[4],
                seen_at=listing[5],
            )

        except Exception as e:
            logger.error(f"Error while getting listing_id:{listing_id}", e)
            return None

    def get_all(self):
        # TODO Remove limit 100
        sql = """
        SELECT * FROM listings LIMIT 100
        """
        try:
            self.database.db_cursor.execute(sql)
            return self.database.db_cursor.fetchall()
        except Exception as e:
            logger.error("Error while getting all listings", e)
            return None

    def create(self, listing: Listing):

        sql = """
        INSERT INTO listings (id, place_id, price, area, room_count, seen_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            self.database.db_cursor.execute(
                sql,
                (
                    listing.listing_id,
                    listing.place_id,
                    listing.price,
                    listing.area,
                    listing.room_count,
                    listing.seen_at,
                ),
            )
            self.database.db.commit()
        except Exception as e:
            self.database.db.rollback()
            logger.error("Error while creating listing", e)
            return None

        logger.debug(f"Successfully created listing_id: {listing.listing_id}")

    def update(self, listing: Listing):
        # Update price and area of apartment in database
        sql = """
        UPDATE listings
        SET price = %s, area = %s, room_count = %s, place_id = %s, seen_at = NOW()
        WHERE id = %s 
        """

        try:
            self.database.db_cursor.execute(
                sql,
                (
                    listing.price,
                    listing.area,
                    listing.room_count,
                    listing.place_id,
                    listing.listing_id,
                ),
            )
            self.database.db.commit()
        except Exception as e:
            self.database.db.rollback()
            logger.debug("Error while updating listing", e)
            return None

        logger.debug("Successfully updated listing_id:", listing.listing_id)
        return listing

    def delete(self, listing_id: int):
        """Delete a listing from id

        Args:
            listing_id (int): listing id
        """

        sql = """
      DELETE FROM listings WHERE id = %s
      """
        try:
            # get listing
            listing = self.get(listing_id)
            if listing is None:
                return None
            self.database.db_cursor.execute(sql, (listing_id,))
            self.database.db.commit()
        except Exception as e:
            self.database.db.rollback()
            logger.error("Error while deleting listing", e)
            return None

        logger.debug("Successfully deleted listing_id:", listing_id)
        return listing_id

    def delete_table_listing(self):
        """Delete table listing"""
        sql = """
      DROP TABLE listings
      """
        try:
            self.database.db_cursor.execute(sql)
            self.database.db.commit()
        except Exception as e:
            self.database.db.rollback()
            logger.error("Error while deleting table listing", e)
            return None

        logger.debug("Successfully deleted table listing")
        return None
