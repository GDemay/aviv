""" This is the CRUD for ListingHistory (create, read, update, delete) """

import logging

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

            logger.debug("Successfully get history_id:", history_id)
            if history is None:
                return None

            return ListingHistory(
                history_id=history[0],
                listing_id=history[1],
                price=history[2],
                date=history[3],
            )

        except Exception as e:
            logger.error(f"Error while getting history_id:{history_id}", e)
            return None

    # Create a new history of the price of a listing
    def create(self, history: ListingHistory):
        """_summary_ : This function create a new history of the price of a listing
        _param_ history : The history of the listing
        _return_ : The history of the listing
        """
        logger.debug("Create history for history_id:", history.history_id)
        if self.get(history.history_id) is not None:
            logging.debug(
                f"History already exists for history_id:{history.history_id}"
            )
            return history

        sql = """
    INSERT INTO history_price (id, listing_id, price, date)
    VALUES (%s, %s, %s, %s)
    """
        try:
            self.database.db_cursor.execute(
                sql,
                (
                    history.history_id,
                    history.listing_id,
                    history.price,
                    history.date,
                ),
            )
            self.database.db_connection.commit()
            logger.debug(
                "Successfully created history_id:", history.history_id
            )
            return history
        except Exception as e:
            logger.error(
                f"Error while creating history_id:{history.history_id}", e
            )
            return None

    # Update the history of the price of a listing
    def update(self, history: ListingHistory):
        """_summary_ : This function update the history of the price of a listing
        _param_ history : The history of the listing
        _return_ : The history of the listing
        """
        logger.debug("Update history for history_id:", history.history_id)
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
            self.database.db_connection.commit()
            logger.debug(
                "Successfully updated history_id:", history.history_id
            )
            return history
        except Exception as e:
            logger.error(
                f"Error while updating history_id:{history.history_id}", e
            )
            return None
