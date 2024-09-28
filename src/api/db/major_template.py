import json
from psycopg2.extras import RealDictCursor
import asyncio

if __name__ == "__main__":
    import connection
else:
    from . import connection

class MajorTemplate:
    
    def __init__(self, db_conn, cache):
        self.db_conn = db_conn
        self.cache = cache

    #Create
    def populate_from_JSON(self):
        pass

    def add_template(self):
        pass

    def add_bulk_template(self):
        pass


    #Read
    def get_by_year(self):
        pass

    def get_by_major(self):
        pass

    def get_by_major_year(self):
        pass


    #Update
    def update_template(self):
        pass

    #Delete
    def remove_by_year(self):
        pass

    def remove_by_major(self):
        pass

    def remove_by_major_year(self):
        pass

