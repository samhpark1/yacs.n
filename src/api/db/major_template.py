import json
from psycopg2.extras import RealDictCursor
import asyncio
import traceback

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

        try:
            with conn.cursor(cursor_factory=RealDictCursor) as transaction:
                for entry in json_data:
                    try:
                        transaction.execute(
                            """
                            INSERT INTO major_template (
                                major,
                                year,
                                school,
                                credits,
                                focus_track,
                                link,
                                notes,
                                required,
                                pick_multiple
                            )
                            VALUES (
                                %(major)s, %(year)s, %(school)s, %(credits)s,
                                %(focus_track)s, %(link)s, %(notes)s, %(required)s,
                                %(pick_multiple)s
                            )
                            ON CONFLICT DO NOTHING;
                            """,
                            {
                                "major": entry['major'],
                                "year": entry['year'],
                                "school": entry['school'],
                                "credits": entry['credits'],
                                "focus_track": entry.get('focus-track', False),
                                "notes": json.dumps(entry['notes']) if not isinstance(entry['notes'], str) else entry['notes'],
                                "link": entry.get('link', None),
                                "required": json.dumps(entry['required']) if not isinstance(entry['required'], str) else entry['required'],
                                "pick_multiple": json.dumps(entry['pick-multiple']) if not isinstance(entry['pick-multiple'], str) else entry['pick-multiple']
                            }
                        )
                    except Exception as e:
                        print("THIS IS THE EXCEPTION:", traceback.format_exc())
                        raise e  # Stop the entire process for debugging purposes

            conn.commit()
            self.clear_cache()
            return (True, "Added Successfully")
        except Exception as e:
            conn.rollback()
            print("ROLLBACK TRIGGERED. Error:", traceback.format_exc())
            return (False, str(e))




    def add_template(self, major, year, school, credits, focus_track,
                    link, notes, required, pick_multiple):
        if year is None or major is None:
            return False, "Year and Major cannot be null"

        
        try:
            # Execute the insert statement without expecting a return
            self.db_conn.execute(
                """
                INSERT INTO major_template (
                    major,
                    year,
                    school,
                    credits,
                    focus_track,
                    link,
                    notes,
                    required,
                    pick_multiple
                )
                VALUES (
                    %(major)s, %(year)s, %(school)s, %(credits)s,
                    %(focus_track)s, %(link)s, %(notes)s, %(required)s,
                    %(pick_multiple)s
                )
                RETURNING*;
                """,
                {
                    "major": major,
                    "year": year,
                    "school": school,
                    "credits": credits,
                    "focus_track": focus_track,
                    "link": link,
                    "notes": notes,
                    "required": required,
                    "pick_multiple": pick_multiple
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

