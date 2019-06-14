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
    def Search_Cloud(cls, region, os, core, diskType, diskCapStart, diskCapEnd, ramStart, ramEnd):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            cloud = None
            query = """SELECT * FROM Clouds 
                    WHERE Region = %s AND OperatingSystem = %s AND Core = %s AND DiskType = %s AND 
                    DiskCapacity >= %s AND DiskCapacity <= %s AND
                    RAM > %s AND RAM <= %s"""
            try:
                cursor.execute(query, (str(region), str(os), str(core), str(diskType), str(diskCapStart), str(diskCapEnd), str(ramStart), str(ramEnd)))
                cloud = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()

            if cloud is not None:
                result = []
                for i in cloud:
                    input = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9]]
                    result.append(input)
                return result
            else:
                return None

    @classmethod
    def Search_Cloud_v2(cls, region, os, core, diskType, diskCapStart, diskCapEnd, ramStart, ramEnd):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()
            cloud = None
            query = "SELECT * FROM Clouds WHERE"
            if region != 0:
                query += "Region = " + region.str() + " AND "
            if os != 0:
                query += "OperatingSystem = " + os.str() + " AND "
            if core != 0:
                query += "Core = " + core.str() + " AND "
            if diskType != 0:
                query += "DiskType = " + diskType.str() + " AND "
            if diskCapEnd != 0:
                query += "DiskCapacity >= " + diskCapStart.str() + " AND " + "DiskCapacity <= " + diskCapEnd.str() + " AND "
            if ramEnd != 0:
                query += "RAM >= " + ramStart.str() + " AND " + "RAM <= " + ramEnd.str() + " AND "

            try:
                cursor.execute(query,)
                cloud = cursor.fetchall()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()
            cursor.close()

            if cloud is not None:
                result = []
                for i in cloud:
                    input = [i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9]]
                    result.append(input)
                return result
            else:
                return None

    def Get_Disk_Capacity(cls, diskCap):
        return {
                '0': 0,
                '128': 0,
                '256': 129,
                '512': 257,
                '1024': 513,
                '2048': 1025,
                '4096': 2049}.get(diskCap, 0)


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

    def Get_Ram_Capacity_v2(cls, ram, cpu):
        if cpu == 1:
            ram_start = 0
            ram_end = 4
        elif cpu == 2:
            ram_start = 3
            ram_end = 16
        elif cpu == 4:
            ram_start = 7
            ram_end = 30
        elif cpu == 8:
            ram_start = 7
            ram_end = 60
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