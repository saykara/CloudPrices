class Jobs:
    @classmethod
    def customer_arrival_job(cls, cloud, request):
        is_enough_vm, is_enough_storage = Jobs.control_availability(cloud, request)

        if is_enough_vm is True and is_enough_storage is True:
            cls.update_providers(cloud=cloud, request=request)
            return True
        # elif is_enough_vm is True and is_enough_storage is False:
        #     pass
        # elif is_enough_vm is False and is_enough_storage is True:
        #     pass
        else:
            return False

    @classmethod
    def update_providers(cls, cloud, request):  #isVM, isSSD
        brand = [i for i in cloud.providers if i.brand == request.brand]
        server = [i for i in brand[0].servers if i.region == request.region and i.os == request.os]

        aimed_server = server[0]
        # if isVM:
        aimed_server.cpu_in_service += request.cpu
        aimed_server.ram_in_service += request.ram
        if request.storage_type == "HDD":
            aimed_server.hdd_storage_in_service += request.storage
        else:
            aimed_server.ssd_storage_in_service += request.storage


    @classmethod
    def control_availability(cls, cloud, request):
        brand = [i for i in cloud.providers if i.brand == request.brand]
        server = [i for i in brand[0].servers if i.region == request.region and i.os == request.os]

        aimed_server = server[0]

        if aimed_server.cpu > request.cpu and aimed_server.ram > request.ram:
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