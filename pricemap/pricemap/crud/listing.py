from pricemap.schemas.listing import Listing
from pricemap.database.session import Database
from flask import Flask, g, render_template
import psycopg2
import requests


class CRUDListing:
    def __init__(self, database):
        self.database = database

    #  self.db = db

    def get(self, listing_id):
        # Get apartment by listing_id
        sql = """
        SELECT * FROM listings WHERE id = %s
        """
        try:
            self.database.db_cursor.execute(sql, (listing_id,))
            listing = self.database.db_cursor.fetchone()
            # Create a new apartment object
            apartment = Listing(
                listing_id=listing[0],
                place_id=listing[1],
                price=listing[2],
                area=listing[3],
                room_count=listing[4],
                seen_at=listing[5],
            )
            return apartment
        except Exception as e:
            print("Error while getting listing_id:" + str(listing_id), e)
            return None

    def get_all(self):
        sql = """
        SELECT * FROM listings LIMIT 100
        """
        try:
            self.database.db_cursor.execute(sql)
            return self.database.db_cursor.fetchall()
        except Exception as e:
            print("Error while getting all listings", e)
            return None

    def create(self, apartment):
        # Insert apartment object in database
        # If apartment already exists, update it

        if self.get(apartment.listing_id) is not None:
            self.update(apartment)
            return apartment

        sql = """
        INSERT INTO listings (id, place_id, price, area, room_count, seen_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            self.database.db_cursor.execute(
                sql,
                (
                    apartment.listing_id,
                    apartment.place_id,
                    apartment.price,
                    apartment.area,
                    apartment.room_count,
                    apartment.seen_at,
                ),
            )
            self.database.db.commit()
        except Exception as e:
            self.database.db.rollback()
            print("Error while creating listing", e)
            return None
        return apartment

    def update(self, apartment):
        # Update price and area of apartment in database
        # TODO le seen_at a un problème
        sql = """
        UPDATE listings
        SET price = %s, area = %s, room_count = %s, place_id = %s, seen_at = NOW()
        WHERE id = %s 
        """

        try:
            self.database.db_cursor.execute(
                sql,
                (
                    apartment.price,
                    apartment.area,
                    apartment.room_count,
                    apartment.place_id,
                    apartment.listing_id,
                ),
            )
            self.database.db.commit()
        except Exception as e:
            self.database.db.rollback()
            print("Error while updating listing", e)
            return None
        return apartment

    # delete table
    def delete(self):
        sql = """
        DROP TABLE listings
        """
        try:
            self.database.db_cursor.execute(sql)
            self.database.db.commit()
        except Exception as e:
            self.database.db.rollback()
            print("Error while deleting table", e)
            return None
        return True
