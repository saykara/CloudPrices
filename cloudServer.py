import parameters
import random


class Provider:
    def __init__(self, brand):
        self.brand = brand
        self.servers = []

    def add_server_into_provider(self, server):
        self.servers.append(server)


class Server:
    def __init__(self, region, os, cpu, ram, hdd, ssd):
        self.region = region
        self.os = os
        self.cpu = cpu
        self.cpu_in_service = 0
        self.ram = ram
        self.ram_in_service = 0
        self.hdd_storage = hdd
        self.hdd_storage_in_service = 0
        self.ssd_storage = ssd
        self.ssd_storage_in_service = 0


class CloudSpace:
    def __init__(self):
        self.providers = []

    def add_provider_into_space(self, provider):
        self.providers.append(provider)

    def create_provider(self, brand):
        provider = Provider(brand)
        self.add_provider_into_space(provider)

    def create_server(self, provider, region, os, cpu, ram, hdd, ssd):
        server = Server(region=region, os=os, cpu=cpu, ram=ram, hdd=hdd, ssd=ssd)
        provider.add_server_into_provider(server)


def create_clouds_randomly():
    space = CloudSpace()
    brand_list = parameters.CloudParameters.brand
    region_list = parameters.CloudParameters.region
    os_list = parameters.CloudParameters.os
    for brand in brand_list:
        provider = Provider(brand)
        for region in region_list:
            for os in os_list:
                server = Server(region=region, os=os, cpu=random.randint(32, 64), ram=random.randint(128, 256),
                                hdd=random.randint(2048, 20480), ssd=random.randint(1024, 10240))
                provider.add_server_into_provider(server)
        space.add_provider_into_space(provider)
    return space
