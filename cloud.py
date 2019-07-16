from database import *


class Cloud:
    def __init__(self, ID, Brand, Region, OperatingSystem, Core, DiskType, DiskCapacity, Price, RAM, BANDWIDTH):
        self.ID = ID
        self.Brand = Brand
        self.Region = Region
        self.OperatingSystem = OperatingSystem
        self.Core = Core
        self.DiskType = DiskType
        self.DiskCapacity = DiskCapacity
        self.Price = Price
        self.RAM = RAM
        self.BANDWIDTH = BANDWIDTH


class CloudOperations:
    @classmethod
    def Search_Cloud(cls, region, os, core, ram):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            cloud = None
            ram_start, ram_end = cls.Get_Ram_Capacity_v2(ram=ram, cpu=core)
            query = """SELECT b.brand, r.region, c.operatingsystem, c.core, c.ram, c.price
                       FROM cloud as c, regions as r, brands as b 
                       WHERE c.brandid = b.id AND c.regionid = r.id AND 
                       regionid = %s AND OperatingSystem = %s AND Core = %s 
                       AND Ram >= %s AND Ram <= %s"""
            try:
                cursor.execute(query, (str(cls.convert_region(region)), str(os), str(core), str(ram_start), str(ram_end)))
                cloud = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()

            if cloud is not None:
                result = []
                for i in cloud:
                    input = [i[0], i[1], i[2], i[3], i[4], i[5]]
                    result.append(input)
                return result
            else:
                return None

    @classmethod
    def Search_Storage(cls, region, storage_type, storage):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            cloud = None
            query = """SELECT b.brand, r.region, s.diskcapacity, s.disktype, s.price 
                       FROM cloud_storage as s, regions as r, brands as b
                       WHERE s.brandid = b.id AND s.regionid = r.id AND 
                       regionid = %s AND diskcapacity = %s AND disktype = %s """
            try:
                cursor.execute(query, (str(cls.convert_region(region)), storage, storage_type))
                cloud = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()

            if cloud is not None:
                result = []
                for i in cloud:
                    input = [i[0], i[1], i[2], i[3], i[4]]
                    result.append(input)
                return result
            else:
                return None

    @classmethod
    def get_all_cloud(cls):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            cloud = None
            query = """SELECT b.brand, r.region, c.operatingsystem, c.core, c.ram, c.price
                           FROM cloud as c, regions as r, brands as b 
                           WHERE c.brandid = b.id AND c.regionid = r.id """
            try:
                cursor.execute(query)
                cloud = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()

            if cloud is not None:
                result = []
                for i in cloud:
                    input = [i[0], i[1], i[2], i[3], i[4], i[5]]
                    result.append(input)
                return result
            else:
                return None

    @classmethod
    def get_all_storage(cls):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            cloud = None
            query = """SELECT b.brand, r.region, s.diskcapacity, s.disktype, s.price 
                           FROM cloud_storage as s, regions as r, brands as b
                           WHERE s.brandid = b.id AND s.regionid = r.id """
            try:
                cursor.execute(query)
                cloud = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()

            if cloud is not None:
                result = []
                for i in cloud:
                    input = [i[0], i[1], i[2], i[3], i[4]]
                    result.append(input)
                return result
            else:
                return None

    @classmethod
    def Get_Disk_Capacity(cls, diskCap):
        return {
                '0': 0,
                '128': 0,
                '256': 129,
                '512': 257,
                '1024': 513,
                '2048': 1025,
                '4096': 2049}.get(diskCap, 0)

    @classmethod
    def Get_Ram_Capacity(cls, ram):
        return {
                '0': 0,
                '1': 0,
                '2': 1,
                '4': 2,
                '8': 4,
                '12': 8,
                '16': 12,
                '32': 16,
                '64': 32,
                '128': 64,
                '4000': 128}.get(ram, 0)

    @classmethod
    def Get_Ram_Capacity_v2(cls, ram, cpu):
        if cpu == 1:
            ram_start = 1
            ram_end = 3
        elif cpu == 2:
            if ram < 8:
                ram_start = 3
                ram_end = 8
            else:
                ram_start = 12
                ram_end = 17
        elif cpu == 4:
            if ram < 16:
                ram_start = 6
                ram_end = 16
            else:
                ram_start = 25
                ram_end = 31
        else:
            ram_start = 0
            ram_end = 0
        return ram_start, ram_end

    def Get_Disk_Bound(cls, diskCap):
        if diskCap <= 128:
            disk_start = 0
            disk_end = 128
        elif diskCap > 128 and diskCap <= 256:
            disk_start = 129
            disk_end = 256
        elif diskCap > 256 and diskCap <= 512:
            disk_start = 257
            disk_end = 512
        elif diskCap > 512 and diskCap <= 1024:
            disk_start = 513
            disk_end = 1024
        elif diskCap > 1024 and diskCap <= 2048:
            disk_start = 1025
            disk_end = 2048
        elif diskCap > 2048 and diskCap <= 4096:
            disk_start = 2049
            disk_end = 4096
        return disk_start, disk_end


    @classmethod
    def convert_brand(cls, brand):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            query = "SELECT id FROM brands WHERE brand like '" + brand + "'"
            try:
                cursor.execute(query)
                brandID = cursor.fetchone()

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            return brandID[0]

    @classmethod
    def convert_region(cls, region):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = "SELECT id FROM regions WHERE region like '" + region + "'"

            try:
                cursor.execute(query)
                regionID = cursor.fetchone()

            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            return regionID[0]
