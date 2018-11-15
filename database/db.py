import sqlite3
from sqlite3 import Error


class Databse():

    # Create the database with tables needed
    def __init__(self, file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        try:
            self.conn = sqlite3.connect(file)
        except Error as e:
            print(e)
        return None

    # Setup the table
    def setup(self):
        """ create sighting table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = self.conn.cursor()
            if c is not None:
                # create sightings table
                sigtings_table = """ CREATE TABLE IF NOT EXISTS sightings (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    original_id integer,
                                    title text,
                                    http_response text,
                                    description text,
                                    detailedDescription text,
                                    altitude text,
                                    city text,
                                    country text,
                                    region text,
                                    zipcode text,
                                    distance text,
                                    duration text,
                                    entityEncountered text,
                                    features text,
                                    flightPath text,
                                    landingOccurred text,
                                    latitude text,
                                    logNumber text,
                                    submitted text,
                                    timeZoneName text,
                                    longitude text,
                                    shape text,
                                    source text
                                ); """
                c.execute(sigtings_table)

                files_table = """ CREATE TABLE IF NOT EXISTS files (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    sighting_id integer,
                                    http_response text,
                                    file_name text,
                                    extension text,
                                    file_type text,
                                    url text
                                ); """
                c.execute(files_table)
            else:
                print("Error! cannot create the database connection.")
        except Error as e:
            print(e)

    # Method to create data
    def add_sighting(self, data):
        conn = sqlite3.connect('database/database.db')
        with conn:
            sql = ''' INSERT INTO sightings(
                                    original_id,
                                    title,
                                    http_response,
                                    description,
                                    detailedDescription,
                                    altitude,
                                    city,
                                    country,
                                    region,
                                    zipcode,
                                    distance,
                                    duration,
                                    entityEncountered,
                                    features,
                                    flightPath,
                                    landingOccurred,
                                    latitude,
                                    logNumber,
                                    submitted,
                                    timeZoneName,
                                    longitude,
                                    shape,
                                    source
                )
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.lastrowid

    def add_bad_data(self, i, error):
        self.add_sighting((
            int(i),
            '',
            error,
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            ''
        ))

    def add_file(self, data):
        conn = sqlite3.connect('database/database.db')
        with conn:
            sql = ''' INSERT INTO files(
                                    sighting_id,
                                    http_response,
                                    file_name,
                                    extension,
                                    file_type,
                                    url
                )
                VALUES(?,?,?,?,?,?) '''
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.lastrowid

    def get_latest_record(self):
        conn = sqlite3.connect('database/database.db')
        cur = conn.cursor()
        with conn:
            latest = cur.execute('SELECT id FROM sightings WHERE id = (SELECT \
            MAX(id) FROM sightings)')

            if latest.fetchall():
                id = cur.execute('SELECT id FROM sightings WHERE id = (SELECT \
                max(id) FROM sightings)').fetchall()[0][0]
                return int(id)
            else:
                return 1  # Empty set
