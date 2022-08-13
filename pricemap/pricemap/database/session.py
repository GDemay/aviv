import psycopg2
from flask import g

from pricemap.core.logger import logger


class Database:
    def __init__(self):
        self.db = g.db
        self.db_cursor = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def init_database(self):
        sql = """
        CREATE TABLE IF NOT EXISTS listings (
            id INTEGER,
            place_id INTEGER,
            price INTEGER,
            area INTEGER,
            room_count INTEGER,
            seen_at TIMESTAMP,
            PRIMARY KEY (id, seen_at)
        );
    """
        self.execute_sql(sql)

    def delete_table(self):
        sql = """
        DROP TABLE listings;
    """
        self.execute_sql(sql)

    def execute_sql(self, sql):
        try:
            self.db_cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error("Error executing SQL", e)
            return
