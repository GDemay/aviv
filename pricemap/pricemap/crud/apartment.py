from pricemap.schemas.apartment import Apartment
from pricemap.database.session import Database
from flask import Flask, g, render_template
import psycopg2
import requests


class CRUDApartment:
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
            return listing
        except Exception as e:
            print("Error: maybe table already exists?", e)
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
            print("Error: maybe table already exists?", e)
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
            print("Error: maybe table already exists?", e)
            return None
        return apartment