import psycopg2 as dbapi2
import os

class DatabaseOperations:
    def __init__(self):
        DATABASE_URL = os.getenv('DATABASE_URL')

        if DATABASE_URL is not None:
            self.config = DATABASE_URL
        else:
            self.config = """user='postgres' password='12345' host='localhost' port=5000 dbname='cloudprices'"""


    def create_tables(self):
        with dbapi2.connect(self.config) as connection:
            cursor = connection.cursor()

            query = "DROP TABLE IF EXISTS Clouds CASCADE"
            cursor.execute(query)

            query = """CREATE TABLE Clouds(
                                            ID SERIAL PRIMARY KEY,
                                            Brand VARCHAR(50),
                                            Region VARCHAR(50),
                                            OperatingSystem VARCHAR(50),
                                            Core INTEGER NOT NULL,
                                            DiskType VARCHAR(50),
                                            DiskCapacity INTEGER NOT NULL,
                                            Price DECIMAL,
                                            RAM DECIMAL NOT NULL,
                                            BANDWIDTH DECIMAL    
                    )"""
            cursor.execute(query)

database = DatabaseOperations()