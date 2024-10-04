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
    def populate_from_JSON(self, json_data):
        conn = self.db_conn.get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as transaction:
            try:
                for entry in json_data:
                    try:
                        self.add_template(entry['major'], entry['year'], entry['classes'])
                    except Exception as e:
                        print("Exception: ", e)
                        conn.rollback()
                        return (False, e)
            except Exception as ve:
                return (False, f"Invalid JSON: {str(ve)}")
        conn.commit()
        self.clear_cache()
        return (True, None)



    def add_template(self, major, year, classes):
        if year is not None and major is not None:
            conn = self.db_conn.get_connection()
            new_template = MajorTemplate(major=major, year=year,classes=classes)
            conn.add(new_template)
            conn.commit()
        return False, "Year and Major cannot be Null."

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
