from pricemap.schemas.apartment import Apartment
from pricemap.database.session import Database
from flask import Flask, g, render_template
import psycopg2
import requests


class CRUDApartment:
    def __init__(self, database):
        self.database = database

    #  self.db = db

    def create(self, apartment):
        # Insert apartment object in database
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
            print("Error: maybe table already exists?", e)
            return None
        return apartment

    def update(self, apartment, logger):
        # Update price and area of apartment in database
        sql = """
        UPDATE listings
        SET price = %s, area = %s, room_count = %s, place_id = %s
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
            print("Error: maybe table already exists?", e)
            return None
        return apartment
