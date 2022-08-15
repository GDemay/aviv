""" This is the CRUD for ListingHistory (create, read, update, delete) """


from pricemap.core.logger import logger
from pricemap.schemas.listing_history import ListingHistory


class CRUDListingHistory:
    """_summary_ : This function the class CRUDListingHistory
    The goal of this class is to create, read,
    update and delete the history of the price of each listing
    """

    # TODO Is this usefull to have database?
    # Maybe we should just call an instance of the database
    def __init__(self, database):
        self.database = database

    def get(self, history_id: int):
        """_summary_ : This function get the listing history of a history
        _param_ history_id : The id of the listing
        _return_ : The history of the listing
        """
        sql = """
    SELECT * FROM history_price WHERE id = %s
    """
        try:
            self.database.db_cursor.execute(sql, (history_id,))
            history = self.database.db_cursor.fetchone()

            if history is None:
                return None

            return ListingHistory(
                history_id=history[0],
                listing_id=history[1],
                price=history[2],
                date=history[3],
            )

        except Exception as e:
            return None

    # Create a new history of the price of a listing
    def create(self, listing_id: int, price: int) -> ListingHistory:
        """This function create a new history of the price of a listing
        _param_  listing_id : The id of the listing
        _param_  price : The price of the listing
        _return_ : The history of the listing
        """

        # Add the new history of the price of the listing
        # Date is automatically added
        # history_id is a new id
        # listing_id is the id of the listing
        # price is the price of the listing
        # date is the date of now

        # Get the last history_price related to listing_id

        logger.debug("Creating a new listing_history!")

        if not listing_id:
            logger.debug("No listing_id")
            return None
        sql = """
        SELECT price FROM history_price WHERE listing_id = %s ORDER BY date DESC limit 1;
        """

        try:
            self.database.db_cursor.execute(sql, (listing_id,))
            old_price = self.database.db_cursor.fetchone()
            # If no history, then price is the price of the listing
            # If there is a history, then price is the price of the last history

            if old_price is not None:
                old_price = old_price[0]
                if old_price == price:
                    logger.debug("Price is the same")
                    return None
                # You can add a new history of the price of the listing

            logger.info("Let's continue!")
            logger.info(f"old_price: {old_price} price: {price}")

        except Exception as e:
            # TODO Improve exception handling that's not good to just return None
            # Exception error should be more
            logger.debug("Error getting old_price")
            logger.debug(e)
            self.database.db.rollback()
            return None

        logger.info("Inserting new history")
        sql = """ INSERT INTO history_price (listing_id, price) VALUES  (%s, %s) RETURNING id """
        try:
            # get history_id
            self.database.db_cursor.execute(sql, (listing_id, price))
            self.database.db.commit()

            history = self.get(self.database.db_cursor.lastrowid)
            logger.debug(f"history: {history}")

            # return self.get(self.database.db_cursor.lastrowid)
        except Exception as e:
            self.database.db.rollback()
            logger.debug(f"Error inserting new history: {e}")
            return None

    # Update the history of the price of a listing
    def update(self, history: ListingHistory):
        """_summary_ : This function update the history of the price of a listing
        _param_ history : The history of the listing
        _return_ : The history of the listing
        """
        if self.get(history.history_id) is None:
            self.create(history)
            return history

        sql = """
    UPDATE history_price
    SET price = %s, date = %s
    WHERE id = %s
    """
        try:
            self.database.db_cursor.execute(
                sql, (history.price, history.date, history.history_id)
            )
            self.database.db.commit()
            return history
        except Exception as e:
            self.database.db.rollback()
            return None
