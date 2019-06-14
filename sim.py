import cloud
import parameters
import random


class Cloud:
    def __init__(self, time, brand, cpu, ram, storageType, storage, region, os, price):
        self.time = time
        self.brand = brand
        self.cpu = cpu
        self.ram = ram
        self.storageType = storageType
        self.storage = storage
        self.region = region
        self.os = os
        self.price = price


def get_price(cloud):
    price = 0
    startRam = cloud.CloudOperations.Get_Ram_Capacity(cloud.ram)
    startStorage = cloud.CloudOperations.Get_Disk_Capacity(cloud.storage)
    cloud.CloudOperations.Search_Cloud(region=cloud.region, ramEnd=cloud.ram, ramStart=startRam, diskCapEnd=cloud.storage,
                                       diskCapStart=startStorage, core=cloud.cpu, diskType=cloud.storageType, os=cloud.os)
    return price


# Random rangini düzenle
def randomly_pick_cloud(time):
    cloud = Cloud()
    cloud.time = time
    cloud.brand = parameters.CloudParameters.brand[random.randint(0, 2)]
    cloud.cpu = parameters.CloudParameters.cpu[random.randint(0, 3)]
    cloud.os = parameters.CloudParameters.operating_system[random.randint(0, 1)]
    cloud.storageType = parameters.CloudParameters.storage_type[random.randint(0, 1)]
    cloud.storage = parameters.CloudParameters.storage_capacity[random.randint(0, 5)]
    cloud.region = parameters.CloudParameters.region[random.randint(0, 4)]
    ram_list = parameters.CloudParameters.ram.get(k=cloud.cpu)
    cloud.ram = ram_list[random.randint(0, len(ram_list))]
    cloud.price = get_price(cloud)
    return cloud


def arrange_fel(number_of_cloud):
    fel = []
    for i in range(number_of_cloud):
        fel.append(randomly_pick_cloud(i))
    return fel


def run_simulation(future_event_list):
    while not future_event_list:
        next_event = future_event_list[0]
        del future_event_list[0]
        clock = next_event.time

           # process