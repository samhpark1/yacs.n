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

    def clear_cache(self):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            loop.create_task(self.cache.clear(namespace="API_CACHE"))
        else:
            asyncio.run(self.cache.clear("API_CACHE"))

    #Create
    def populate_from_JSON(self, json_data):
        conn = self.db_conn.get_connection()
        
        with conn.cursor(cursor_factory=RealDictCursor) as transaction:
            try:
                for entry in json_data:
                    try:
                        transaction.execute(
                            """
                            INSERT INTO major_template (
                                major,
                                year,
                                classes
                            )
                            VALUES (
                                %(major)s, %(year)s, %(classes)s
                            )
                            ON CONFLICT DO NOTHING;
                            """,
                            {
                                "major": entry['major'],
                                "year": entry['year'],
                                "classes": json.dumps(entry['classes'])
                            }
                        )
                    except Exception as e:
                        print("THIS IS THE EXCEPTION:", e)
                        conn.rollback()
                        return (False, e)
            except ValueError as ve:
                return (False, f"Invalid JSON data: {str(ve)}")

            conn.commit()

            self.clear_cache()

            return (True, "Added Successfully")




    def add_template(self, major, year, classes):
        if year is None or major is None or classes is None:
            return False, "Year, Major, and Classes cannot be null"

        
        try:
            # Execute the insert statement without expecting a return
            self.db_conn.execute(
                """
                INSERT INTO major_template (
                    major,
                    year,
                    classes
                )
                VALUES (
                    %(major)s, %(year)s, %(classes)s
                )
                RETURNING*;
                """,
                {
                    "major": major,
                    "year": year,
                    "classes": classes
                }, False
            )

            return True, None  # Successfully inserted
        except Exception as e:
            # Catch any unexpected errors
            print(f"Unexpected error: {e}")
            return False, f"An unexpected error occurred: {str(e)}"


    #Read
    def get_all(self):
        try:
            result = self.db_conn.execute(
                """
                    SELECT * FROM major_template
                """,
                ()
            )

            return result
        except Exception as e:
            return False, e


    def get_by_year(self, year):
        if year is not None:
            result = self.db_conn.execute(
                """
                    SELECT *
                    FROM major_template
                    WHERE year = %s
                """,
                (year, )
            )
            print(result)
            return result
        return False, "Year cannot be null"

    def get_by_major(self, major):
        if major is not None:
            return self.db_conn.execute(
                """
                    SELECT *
                    FROM major_template
                    WHERE major = %s
                """,
                (major,),
                True
            )
        return False, "Major cannot be null"

    def get_by_major_year(self, major, year):
        if major is not None and year is not None:
            return self.db_conn.execute(
                """
                    SELECT *
                    FROM major_template
                    WHERE major = %(major)s AND year = %(year)s
                """,
                {
                    "major": major,
                    "year": year,
                },
                True
            )
        return False, "Major and Year cannot be null"



    #Delete
    def remove_by_year(self, year):
        if year is not None:
            return True, self.db_conn.execute(
                """
                    DELETE FROM major_template
                    WHERE year = %s
                """,
                (year,),
                False
            )
        return False, "Year cannot be null"

    def remove_by_major(self, major):
        if major is not None:
            return True, self.db_conn.execute(
                """
                    DELETE FROM major_template
                    WHERE major = %s
                """,
                (major,),
                False
            )
        return False, "Major cannot be null"

    def remove_by_major_year(self, major, year):
        if major is not None and year is not None:
            return True, self.db_conn.execute(
                """
                    DELETE FROM major_template
                    WHERE major = %(major)s AND year = %(year)s
                """,
                {"major": str(major), "year": int(year)},
                False
            )
        return False, "Major and Year cannot be null"

    def remove_all(self):
        try:
            return True, self.db_conn.execute(
                """
                    DELETE FROM major_template
                """,
                {},
                False
            )
        except Exception as e:
            return False, e

