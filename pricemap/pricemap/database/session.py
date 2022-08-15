""" Init database cursor and set it to a Database class and handle some SQL requests"""
import psycopg2
from flask import g

from pricemap.core.logger import logger


class Database:
    """Class Database that handles SQL requests"""

    def __init__(self) -> None:
        """Set some atributes to database"""
        self.db = g.db
        self.db_cursor = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def init_listing_table(self) -> None:
        """
        summary: It creates a new table if it does not exists.

        listing_id: id of listing
        place_id : arrondissement of paris with an id (geom)
        price: price of the listing
        area: area of the listing
        room_count: number of rooms in the listing
        creation_date : date of creation of the listing
        deleted_at: date of deletion of the listing
        active: if the listing is active or not
        (using for deletion because we don't want to delete the listing from the database just set active to false)
        """

        sql = """
    CREATE TABLE IF NOT EXISTS listings (
        listing_id INTEGER,
        place_id INTEGER,
        price INTEGER,
        area INTEGER,
        room_count INTEGER,
        creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        deleted_at TIMESTAMP,
        PRIMARY KEY (listing_id)
    );
  """
        self.execute_sql(sql)

    def init_history_price_table(self) -> None:
        """This function create a new table that will contain the history of the price of each listing"""
        # This function create a new table that will contain the history of the price of each listing
        # There is a few fields like : id (auto_increment), listing_id (the id of the listing from listing table), price (the price of the listing), date (the date when the price was seen)

        sql = """
    CREATE TABLE IF NOT EXISTS history_price (
        id SERIAL,
        listing_id INTEGER,
        price INTEGER,
        date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (id)
    );
    """
        self.execute_sql(sql)

    def delete_table(self):
        sql = """
      DROP TABLE IF EXISTS listings;
  """
        try:
            self.execute_sql(sql)
        except Exception as e:
            logger.error("Error deleting table", e)
            return {"error": "Error deleting table"}
        return {"message": "Table deleted"}

    def execute_sql(self, sql):
        try:
            self.db_cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error("Error executing SQL", e)
            return
