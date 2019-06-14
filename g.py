import parameters
import random
import cloud


class Provider:
    brand = ""
    servers = []


class Server:
    region = ""
    os = ""
    cpu = 0
    cpu_in_service = 0
    ram = 0
    ram_in_service = 0
    hdd_storage = 0
    hdd_storage_in_service = 0
    ssd_storage = 0
    ssd_storage_in_service = 0


def create_provider_randomly():
    brand_list = parameters.CloudParameters.brand
    region_list = parameters.CloudParameters.region
    os_list = parameters.CloudParameters.operating_system
    provider_list = []

    for brand in brand_list:
        provider = Provider()
        provider.brand = brand
        for region in region_list:
            for os in os_list:
                server = Server()
                server.os = os
                server.region = region
                server.cpu = random.randomint(4, 32)
                server.ram = random.randomint(32, 256)
                server.hdd_storage = random.randomint(1024, 10240)
                server.ssd_storage = random.randomint(1024, 10240)
                provider.servers.append(server)

        provider_list.append(provider)
    return provider_list


def add_server_to_provider_manuel(provider, region, cpu, ram, hdd, ssd):
    server = Server()
    server.region = region
    server.cpu = cpu
    server.ram = ram
    server.hdd_storage = hdd
    server.ssd_storage = ssd
    provider.servers.append(server)

    return provider


def create_provider_manuel(brand):
    provider = Provider()
    provider.brand = brand
    return provider


def controlling_enough_capacity(provider, event):
    if provider.cpu > event.cpu and provider.ram > event.ram:
        isEnoughVM = True
    else:
        isEnoughVM = False

    if event.storageType == "SSD":
        if (provider.ssd_storage - provider.ssd_storage_in_service) > event.storage:
            isEnoughStorage = True
        else:
            isEnoughStorage = False
    else:
        if (provider.hdd_storage - provider.hdd_storage_in_service) > event.storage:
            isEnoughStorage = True
        else:
            isEnoughStorage = False

    return isEnoughVM, isEnoughStorage


def controlling_enough_capacity_v2(providers, cloud, event):
    brand_index = [i for i in providers if i.brand == cloud[1]]
    server_index = [i for i in providers[brand_index] if i.region == cloud[2] and i.os == cloud[3]]
    if providers[brand_index][server_index].cpu > event.cpu and providers[brand_index][server_index].ram > event.ram:
        isEnoughVM = True
    else:
        isEnoughVM = False

    if event.storageType == "SSD":
        if (providers[brand_index][server_index].ssd_storage - providers[brand_index][server_index].ssd_storage_in_service) > event.storage:
            isEnoughStorage = True
        else:
            isEnoughStorage = False
    else:
        if (providers[brand_index][server_index].hdd_storage - providers[brand_index][server_index].hdd_storage_in_service) > event.storage:
            isEnoughStorage = True
        else:
            isEnoughStorage = False

    return isEnoughVM, isEnoughStorage


def update_providers(providers, event, isVM, isSSD, updateInfo):
    brand_index = [i for i in providers if i.brand == updateInfo[0]]
    server_index = [i for i in providers[brand_index] if i.region == updateInfo[1] and i.os == updateInfo[2]]

    if isVM:
        providers[brand_index][server_index].cpu_in_service += event.cpu
        providers[brand_index][server_index].ram_in_service += event.ram
    if isSSD:
        providers[brand_index][server_index].ssd_in_service += event.storage
    if not isSSD:
        providers[brand_index][server_index].ssd_in_service += event.storage
    return providers


def find_alternative_vm_cloud(providers, event):
    start_ram, end_ram = cloud.CloudOperations.Get_Ram_Capacity_v2(event.ram, event.cpu)
    start_disk, end_disk = cloud.CloudOperations.Get_Disk_Bound(event.storage)
    clouds = cloud.CloudOperations.Search_Cloud(os=event.os, diskType=event.storageType, core=event.cpu, diskCapStart=start_disk,
                                       diskCapEnd=end_disk, ramStart=start_ram, ramEnd=end_ram)
    # Oyun ve Marjinal fayda
    clouds.sort(key=lambda x: x[7])
    for i in clouds:
        isEnoughVM, isEnoughStorage = controlling_enough_capacity_v2(providers, i, event)
        if isEnoughVM:
            return [i[1], i[2], i[3]]


def find_alternative_storage_cloud(event):
    # SQL search
    return []


def process(providers, event):
    matched_brand = (x for x in providers if x.brand == event.brand)
    matched_region_os = (y for y in matched_brand if y.region == event.region and y.os == event.os)

    isEnoughVM, isEnoughStorage = controlling_enough_capacity(matched_region_os, event)
    if event.storageType == "SSD":
        isSSD = True
    else:
        isSSD = False


    if isEnoughVM is True and isEnoughStorage is True:
        providers = update_providers(providers, event, True, isSSD, [event.brand, event.region, event.os])
    elif isEnoughVM is True and isEnoughStorage is False:
        providers = update_providers(providers, event, True, None, [event.brand, event.region, event.os])
        providers = update_providers(providers, event, False, isSSD, find_alternative_vm_cloud(providers, event))
        # Find storage (Database ayarlandıktan sonra değişecek)
        # find_alternative_storage_cloud(event)
    elif isEnoughVM is False and isEnoughStorage is True:
        providers = update_providers(providers, event, False, isSSD, [event.brand, event.region, event.os])
        providers = update_providers(providers, event, True, None, find_alternative_vm_cloud(providers, event))
    else:
        # Find storage (Database ayarlandıktan sonra değişecek)
        # find_alternative_storage_cloud(event)
        providers = update_providers(providers, event, False, isSSD, find_alternative_vm_cloud(providers, event))
        providers = update_providers(providers, event, True, None, find_alternative_vm_cloud(providers, event))
    return providers