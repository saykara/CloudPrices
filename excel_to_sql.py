import psycopg2 as dbapi2
import xlrd
from database import *

class ExcelOperations:
    def transfer(self):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            book = xlrd.open_workbook("Cloud.xlsx")
            sheet = book.sheet_by_name("Sayfa1")

            query = """INSERT INTO Clouds (Brand, Region, OperatingSystem, Core, DiskType, DiskCapacity, Price, RAM) 
                                                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

            for r in range(1, sheet.nrows):
                Brand = sheet.cell(r, 0).value
                Region = sheet.cell(r, 1).value
                OperatingSystem = sheet.cell(r, 2).value
                Core = sheet.cell(r, 3).value
                DiskType = sheet.cell(r, 4).value
                DiskCapacity = sheet.cell(r, 5).value
                RAM = sheet.cell(r, 6).value
                Price = sheet.cell(r, 7).value

                values = (Brand, Region, OperatingSystem, Core, DiskType, DiskCapacity, Price, RAM)

                cursor.execute(query, values)
            connection.commit()
            cursor.close()
            return

