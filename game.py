import cloud as cl
import copy

class Jobs:
    @classmethod
    def customer_arrival_job(cls, cloud, request):
        is_enough_vm, is_enough_storage = Jobs.control_availability(cloud, request)

        if is_enough_vm is True and is_enough_storage is True:
            cls.update_providers(cloud=cloud, request=request, isVM=True, isStorage=True)
            return True, is_enough_vm, is_enough_storage
        else:
            return False, is_enough_vm, is_enough_storage

    @classmethod
    def update_providers(cls, cloud, request, isVM, isStorage):
        brand = [i for i in cloud.providers if i.brand == request.brand]
        server = [i for i in brand[0].servers if i.region == request.region and i.os == request.os]

        aimed_server = server[0]
        # if isVM:
        aimed_server.cpu_in_service += request.cpu
        aimed_server.ram_in_service += request.ram
        # if isStorage:
        if request.storage_type == "HDD":
            aimed_server.hdd_storage_in_service += request.storage
        else:
            aimed_server.ssd_storage_in_service += request.storage


    @classmethod
    def control_availability(cls, cloud, request):
        brand = [i for i in cloud.providers if i.brand == request.brand]
        server = [i for i in brand[0].servers if i.region == request.region and i.os == request.os]

        aimed_server = server[0]

        if aimed_server.cpu - aimed_server.cpu_in_service > request.cpu and aimed_server.ram - aimed_server.ram_in_service > request.ram:
            is_enough_vm = True
        else:
            is_enough_vm = False

        if request.storage_type == "SSD":
            if (aimed_server.ssd_storage - aimed_server.ssd_storage_in_service) > request.storage:
                is_enough_storage = True
            else:
                is_enough_storage = False
        else:
            if (aimed_server.hdd_storage - aimed_server.hdd_storage_in_service) > request.storage:
                is_enough_storage = True
            else:
                is_enough_storage = False

        return is_enough_vm, is_enough_storage

    @classmethod
    def erase_server_job(cls, cloud, request):
        brand = [i for i in cloud.providers if i.brand == request.brand]
        server = [i for i in brand[0].servers if i.region == request.region and i.os == request.os]

        aimed_server = server[0]
        # if isVM:
        aimed_server.cpu_in_service -= request.cpu
        aimed_server.ram_in_service -= request.ram
        if request.storage_type == "HDD":
            aimed_server.hdd_storage_in_service -= request.storage
        else:
            aimed_server.ssd_storage_in_service -= request.storage

    @classmethod
    def find_provider_job(cls, cloud, request, vm_db, vm_sto):
        if request.cpu is not 0 and request.ram is not 0:
            providers = cls.search_vm(request, vm_db)
            providers.sort(key=lambda x: x[5])
        else:
            providers = cls.search_sto(request, vm_sto)
            providers.sort(key=lambda x: x[4])

        for i in providers:
            if i[0] != request.brand:
                temp_request = copy.copy(request)
                temp_request.brand = i[0]
                isEnoughVM, isEnoughStorage = cls.control_availability(cloud, temp_request)
                if isEnoughVM and isEnoughStorage:
                    return temp_request
        return False

    @classmethod
    def search_vm(cls, request, cloud_DB_VM):
        result = []
        for i in cloud_DB_VM:
            ram_start, ram_end = cl.CloudOperations.Get_Ram_Capacity_v2(ram=request.ram, cpu=request.cpu)
            if i[1] == request.region and i[2] == request.os and i[3] == request.cpu and i[4] >= ram_start and i[4] <= ram_end:
                result.append(i)
        if not result:
            return False
        else:
            return result

    @classmethod
    def search_sto(cls, request, cloud_DB_sto):
        result = []
        for i in cloud_DB_sto:
            if i[1] == request.region and i[2] == request.storage and i[3] == request.storage_type:
                result.append(i)
        if not result:
            return False
        else:
            return result
