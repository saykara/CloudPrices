import psycopg2 as dbapi2
import os
import parameters


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

            query = "DROP TABLE IF EXISTS Brands CASCADE"
            cursor.execute(query)

            query = """CREATE TABLE Brands(
                                            ID SERIAL PRIMARY KEY,
                                            Brand VARCHAR(50) 
                                                        )"""
            cursor.execute(query)

            query = "DROP TABLE IF EXISTS Regions CASCADE"
            cursor.execute(query)

            query = """CREATE TABLE Regions(
                                             ID SERIAL PRIMARY KEY,
                                             Region VARCHAR(50)  
                                                                    )"""
            cursor.execute(query)

            query = "DROP TABLE IF EXISTS Cloud CASCADE"
            cursor.execute(query)

            query = """CREATE TABLE Cloud(
                                            ID SERIAL PRIMARY KEY,
                                            BrandID INTEGER NOT NULL,
                                            RegionID INTEGER NOT NULL,
                                            OperatingSystem VARCHAR(50),
                                            Core INTEGER NOT NULL,
                                            RAM DECIMAL NOT NULL,
                                            Price DECIMAL,
                                            FOREIGN KEY (BrandID) REFERENCES Brands(ID) ON DELETE RESTRICT,
                                            FOREIGN KEY (RegionID) REFERENCES Regions(ID) ON DELETE RESTRICT
                    )"""
            cursor.execute(query)

            query = "DROP TABLE IF EXISTS Cloud_Storage CASCADE"
            cursor.execute(query)

            query = """CREATE TABLE Cloud_Storage(
                                             ID SERIAL PRIMARY KEY,
                                             BrandID INTEGER NOT NULL,
                                             RegionID INTEGER NOT NULL,
                                             DiskCapacity INTEGER NOT NULL,
                                             DiskType VARCHAR(50),
                                             Price DECIMAL,
                                             FOREIGN KEY (BrandID) REFERENCES Brands(ID) ON DELETE RESTRICT,
                                             FOREIGN KEY (RegionID) REFERENCES Regions(ID) ON DELETE RESTRICT
                                )"""
            cursor.execute(query)

    def db_init_parameters(self):
        with dbapi2.connect(self.config) as connection:
            cursor = connection.cursor()

            query = """INSERT INTO Brands(Brand) VALUES (%(brand)s)"""
            cursor.executemany(query, parameters.DatabaseParameters.brand_dict)

            query = """INSERT INTO Regions(Region) VALUES (%(region)s)"""
            cursor.executemany(query, parameters.DatabaseParameters.region_dict)


database = DatabaseOperations()