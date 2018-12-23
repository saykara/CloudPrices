import psycopg2 as dbapi2
import os

class DatabaseOperations:
    def __init__(self):

        DATABASE_URL = os.getenv('DATABASE_URL')

        if DATABASE_URL is not None:
            self.config = DATABASE_URL
        else:
            self.config = """user='postgres' password='12345' host='localhost' port=5432 dbname='cloudprices'"""


    def create_tables(self):
        with dbapi2.connect(self.config) as connection:
            cursor = connection.cursor()

            query = "DROP TABLE IF EXISTS Parameters CASCADE"
            cursor.execute(query)

            query = """CREATE TABLE Parameters(
                                                    ID SERIAL PRIMARY KEY,
                                                    Name VARCHAR(50)
                            )"""
            cursor.execute(query)

            query = "DROP TABLE IF EXISTS Clouds CASCADE"
            cursor.execute(query)

            query = """CREATE TABLE Clouds(
                                            ID SERIAL PRIMARY KEY,
                                            Brand VARCHAR(50),
                                            RegionID INTEGER NOT NULL,
                                            OperatingSystem VARCHAR(50),
                                            Core INTEGER NOT NULL,
                                            DiskType VARCHAR(50),
                                            DiskCapacity INTEGER NOT NULL,
                                            Price DECIMAL NOT NULL,
                                            RAM DECIMAL NOT NULL,
                                            BANDWIDTH DECIMAL,
                                            FOREIGN KEY (RegionID) REFERENCES Parameters(ID)                  
                    )"""
            cursor.execute(query)

