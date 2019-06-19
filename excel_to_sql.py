import xlrd
from database import *
import cloud


class ExcelOperations:
    @classmethod
    def transfer_cloud(cls):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            print("Transfer operation started..")
            book = xlrd.open_workbook("documents/Cloud2.xlsx")
            sheet = book.sheet_by_name("Sayfa1")

            query = """INSERT INTO Cloud (BrandID, RegionID, OperatingSystem, Core, RAM, Price) 
                                                                        VALUES (%s, %s, %s, %s, %s, %s)"""

            for r in range(1, sheet.nrows):
                Brand = sheet.cell(r, 0).value
                Region = sheet.cell(r, 1).value
                OperatingSystem = sheet.cell(r, 2).value
                Core = sheet.cell(r, 3).value
                RAM = sheet.cell(r, 4).value
                Price = sheet.cell(r, 5).value
                bra = cloud.CloudOperations.convert_brand(Brand)
                values = (cloud.CloudOperations.convert_brand(Brand), cloud.CloudOperations.convert_region(Region), OperatingSystem, Core, RAM, Price)

                cursor.execute(query, values)
            connection.commit()
            cursor.close()
            print("Cloud transfer operation ended..")
            return

    @classmethod
    def transfer_storage(cls):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            print("Storage transfer operation started..")
            book = xlrd.open_workbook("documents/Cloud2.xlsx")
            sheet = book.sheet_by_name("Sayfa2")

            query = """INSERT INTO Cloud_Storage (BrandID, RegionID, DiskCapacity, DiskType, Price) 
                                                                        VALUES (%s, %s, %s, %s, %s)"""

            for r in range(1, sheet.nrows):
                Brand = sheet.cell(r, 0).value
                Region = sheet.cell(r, 1).value
                DiskType = sheet.cell(r, 2).value
                DiskCapacity = sheet.cell(r, 3).value
                Price = sheet.cell(r, 4).value

                values = (cloud.CloudOperations.convert_brand(Brand), cloud.CloudOperations.convert_region(Region), DiskCapacity, DiskType, Price)

                cursor.execute(query, values)
            connection.commit()
            cursor.close()
            print("Storage transfer operation ended..")
            return

