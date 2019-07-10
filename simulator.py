import random
import cloudServer
import cloud
import parameters
import game
import copy
import matplotlib.pyplot as plt
import tree
import matplotlib.animation as ani
import time


class CloudRequest:
    def __init__(self, brand, region, os, cpu, ram, storage_type, storage):
        self.brand = brand
        self.region = region
        self.os = os
        self.cpu = cpu
        self.ram = ram
        self.storage_type = storage_type
        self.storage = storage


cloud_DB_VM = []
cloud_DB_sto = []


class Simulator:
    global cloud_DB_VM
    global cloud_DB_sto
    cust_start = 0
    cust_end = 0
    exp_start = 0
    exp_end = 0

    fundamental_price_list = []
    customer_list = []
    current_rate = []
    rate_history = []
    gantt_list = []
    out_list = []
    reject_list = []

    def __init__(self):
        self.fel = []
        self.cloud = None
        self.state = None

    class Event:
        def __init__(self, event_time, detail):
            self.event_time = event_time
            self.detail = detail

        def process(self, fel, cloud, clock, state):
            raise NotImplementedError

    class CustomerArrivalEvent(Event):
        def __init__(self, event_time, detail):
            super().__init__(event_time, detail)

        def process(self, fel, cloud, clock, state):
            Simulator.customer_list.append(self.detail.brand)
            result, is_enough_vm, is_enough_storage = game.Jobs.customer_arrival_job(cloud=cloud, request=self.detail)
            if not result:
                if not is_enough_storage and not is_enough_vm:
                    state['cum'] += 1
                    fel.append(Simulator.OutsourceCloud(event_time=clock, detail=self.detail))
                elif not is_enough_vm:
                    state['vm'] += 1
                    fel.append(Simulator.OutsourceVM(event_time=clock, detail=self.detail))
                elif not is_enough_storage:
                    state['sto'] += 1
                    fel.append(Simulator.OutsourceStorage(event_time=clock, detail=self.detail))
            else:
                time = clock + Simulator.cloud_expired_time()
                fel.append(Simulator.CloudExpiredEvent(event_time=clock + Simulator.cloud_expired_time(),
                                                       detail=self.detail))
                Simulator.gantt_list.append([clock, time])
                state['successful'] += 1
            fel.append(Simulator.CustomerArrivalEvent(event_time=clock + Simulator.customer_inter_arrival_time(),
                                                      detail=Simulator.create_request_automatically()))

    class CloudExpiredEvent(Event):
        def __init__(self, event_time, detail):
            super().__init__(event_time, detail)

        def process(self, fel, cloud, clock, state):
            game.Jobs.erase_server_job(cloud=cloud, request=self.detail)
            state['erase_count'] += 1

    class OutsourceCloud(Event):
        def __init__(self, event_time, detail):
            super().__init__(event_time, detail)

        def process(self, fel, cloud, clock, state):
            new_request = copy.copy(self.detail)
            new_request.storage = 0
            self.detail.ram = 0
            self.detail.cpu = 0
            global cloud_DB_sto
            global cloud_DB_VM

            updated_request_vm = game.Jobs.find_provider_job(cloud, new_request, cloud_DB_VM, cloud_DB_sto)
            updated_request_sto = game.Jobs.find_provider_job(cloud, self.detail, cloud_DB_VM, cloud_DB_sto)

            if updated_request_vm and updated_request_sto:
                time = clock + Simulator.cloud_expired_time()

                result, is_enough_vm, is_enough_storage = game.Jobs.customer_arrival_job(cloud=cloud,
                                                                                         request=updated_request_vm)
                if result:
                    fel.append(Simulator.CloudExpiredEvent(event_time=time, detail=updated_request_vm))

                result, is_enough_vm, is_enough_storage = game.Jobs.customer_arrival_job(cloud=cloud,
                                                                                         request=updated_request_sto)
                if result:
                    fel.append(Simulator.CloudExpiredEvent(event_time=time, detail=updated_request_sto))
                state['out_cum'] += 1
                Simulator.out_list.append([len(Simulator.gantt_list), clock])
            if not updated_request_vm and not updated_request_sto:
                state['fail'] += 1
                Simulator.reject_list.append([len(Simulator.gantt_list),clock])

    class OutsourceVM(Event):
        def __init__(self, event_time, detail):
            super().__init__(event_time, detail)

        def process(self, fel, cloud, clock, state):
            new_request = copy.copy(self.detail)
            new_request.storage = 0
            self.detail.ram = 0
            self.detail.cpu = 0
            global cloud_DB_sto
            global cloud_DB_VM

            updated_request = game.Jobs.find_provider_job(cloud, new_request, cloud_DB_VM, cloud_DB_sto)

            if updated_request:
                time = clock + Simulator.cloud_expired_time()

                result, is_enough_vm, is_enough_storage = game.Jobs.customer_arrival_job(cloud=cloud, request=self.detail)
                if result:
                    fel.append(Simulator.CloudExpiredEvent(event_time=time, detail=self.detail))

                result, is_enough_vm, is_enough_storage = game.Jobs.customer_arrival_job(cloud=cloud, request=updated_request)
                if result:
                    fel.append(Simulator.CloudExpiredEvent(event_time=time, detail=updated_request))
                state['out_vm'] += 1
                Simulator.out_list.append([len(Simulator.gantt_list), clock])
            else:
                state['fail'] += 1
                Simulator.reject_list.append([len(Simulator.gantt_list), clock])

    class OutsourceStorage(Event):
        def __init__(self, event_time, detail):
            super().__init__(event_time, detail)

        def process(self, fel, cloud, clock, state):
            new_request = copy.copy(self.detail)
            new_request.cpu = 0
            new_request.ram = 0
            self.detail.storage = 0
            global cloud_DB_sto
            global cloud_DB_VM

            updated_request = game.Jobs.find_provider_job(cloud, new_request, cloud_DB_VM, cloud_DB_sto)

            if updated_request:
                time = clock + Simulator.cloud_expired_time()

                result, is_enough_vm, is_enough_storage = game.Jobs.customer_arrival_job(cloud=cloud,
                                                                                         request=self.detail)
                if result:
                    fel.append(Simulator.CloudExpiredEvent(event_time=time, detail=self.detail))

                result, is_enough_vm, is_enough_storage = game.Jobs.customer_arrival_job(cloud=cloud,
                                                                                         request=updated_request)
                if result:
                    fel.append(Simulator.CloudExpiredEvent(event_time=time, detail=updated_request))
                state['out_sto'] += 1
                Simulator.out_list.append([len(Simulator.gantt_list), clock])
            else:
                state['fail'] += 1
                Simulator.reject_list.append([len(Simulator.gantt_list), clock])

    class UpdatePolicyEvent(Event):
        def __init__(self, event_time, detail):
            super().__init__(event_time, detail)

        def process(self, fel, cloud, clock, state):
            Simulator.change_policy(self.detail)
            fel.append(Simulator.UpdatePolicyEvent(event_time=clock + 500, detail=self.detail))

    class UpdatePolicyHistory(Event):
        def __init__(self, event_time, detail):
            super().__init__(event_time, detail)

        def process(self, fel, cloud, clock, state):
            Simulator.update_rate()
            fel.append(Simulator.UpdatePolicyHistory(event_time=clock + 500, detail=self.detail))

    @classmethod
    def fel_key(cls, event):
        return event.event_time

    def create_cloud_randomly(self):
        self.cloud = cloudServer.create_clouds_randomly()

    def simulation(self, range):
        clock = 0
        Simulator.create_db()
        self.create_cloud_randomly()
        self.fel.append(self.CustomerArrivalEvent(event_time=clock, detail=self.create_request_automatically()))
        Simulator.initialize_policy_events(self.fel)
        self.state = {'successful': 0, 'erase_count': 0, 'vm': 0, 'sto': 0, 'cum': 0, 'out_cum': 0, 'out_vm': 0, 'out_sto': 0, 'fail': 0}

        while self.fel and self.state['successful'] + self.state['cum'] + self.state['vm'] + self.state['sto'] < range:
            self.fel.sort(key=self.fel_key)
            next_event = self.fel[0]
            del self.fel[0]
            clock = next_event.event_time
            next_event.process(fel=self.fel, clock=clock, cloud=self.cloud, state=self.state)
        Simulator.fundamental_price_list = Simulator.get_starting_fundamental_prices()
        Simulator.erase_db()
        self.print_outputs(range)

    def print_outputs(self, range):
        print("Successful without Outsource: ", self.state['successful'])
        print("Successful with Outsource: ", range - self.state['fail'])
        print("Unsuccessful without Outsource: ", self.state['cum'] + self.state['vm'] + self.state['sto'])
        print("Unsuccessful with Outsource: ", self.state['fail'])
        print("Erase: ", self.state['erase_count'])
        print("Lack of VM: ", self.state['vm'])
        print("Lack of Storage: ", self.state['sto'])
        print("Lack of Both: ", self.state['cum'])
        print("Outsource of VM: ", self.state['out_vm'])
        print("Outsource of Storage: ", self.state['out_sto'])
        print("Outsource of Both: ", self.state['out_cum'])

    @classmethod
    def initialize_parameters(cls, c_s, c_e, e_s, e_e):
        cls.current_rate = [0, 0, 0]
        cls.exp_start = e_s
        cls.exp_end = e_e
        cls.cust_start = c_s
        cls.cust_end = c_e

    @classmethod
    def initialize_policy_events(cls, fel):
        brands = parameters.CloudParameters.brand
        clock = 400
        for i in brands:
            fel.append(Simulator.UpdatePolicyEvent(event_time=clock, detail=i))
            clock += 50
        fel.append(Simulator.UpdatePolicyHistory(event_time=clock, detail=None))

    @classmethod
    def create_db(cls):
        global cloud_DB_sto
        global cloud_DB_VM
        cloud_DB_VM = cloud.CloudOperations.get_all_cloud()
        cloud_DB_sto = cloud.CloudOperations.get_all_storage()

    @classmethod
    def erase_db(cls):
        global cloud_DB_sto
        global cloud_DB_VM
        del cloud_DB_sto
        del cloud_DB_VM

    @classmethod
    def customer_inter_arrival_time(cls):
        return random.uniform(Simulator.cust_start, Simulator.cust_end)

    @classmethod
    def cloud_expired_time(cls):
        return random.uniform(Simulator.exp_start, Simulator.exp_end)

    @classmethod
    def create_request_automatically(cls):
        par = parameters.CloudParameters()
        cpu = random.choice(par.cpu)
        ram = random.choice(par.ram[str(cpu)])
        result = CloudRequest(brand=None, os=random.choice(par.os), region=random.choice(par.region),
                              cpu=cpu, ram=ram, storage_type=random.choice(par.s_type),
                              storage=random.choice(par.s_capacity))
        return cls.pick_brand_biased(result)

    @classmethod
    def pick_brand_biased(cls, request):
        global cloud_DB_sto
        global cloud_DB_VM
        vms = game.Jobs.search_vm(request, cloud_DB_VM)
        stos = game.Jobs.search_sto(request, cloud_DB_sto)
        request_price = []
        sum = 0

        for vm in vms:
            for sto in stos:
                if vm[0] == sto[0]:
                    request_price.append([vm[0], (float(vm[5]) + float(sto[4])) + ((float(vm[5]) + float(sto[4])) * cls.find_rate(vm[0]) / 100), 0])
                    sum += float(vm[5]) + float(sto[4])

        for i in range(0, len(request_price)):
            request_price[i][2] = (request_price[(i + 1)%3][1] + request_price[(i + 2)%3][1])/(2 * sum)

        rand_num = random.uniform(0,1)

        if request_price[0][2] > rand_num:
            request.brand = request_price[0][0]
        elif request_price[0][2] + request_price[1][2] > rand_num:
            request.brand = request_price[1][0]
        else:
            request.brand = request_price[2][0]
        return request

    @classmethod
    def change_policy(cls, brand):
        request = CloudRequest(brand=None, region="US East", os="Windows", cpu=1, ram=2, storage=256, storage_type="SSD")
        vms = game.Jobs.search_vm(request, cloud_DB_VM)
        stos = game.Jobs.search_sto(request, cloud_DB_sto)
        request_price = []
        sum = 0

        for vm in vms:
            for sto in stos:
                if vm[0] == sto[0]:
                    request_price.append([vm[0], vm[5] + sto[4], 0])

        list = []
        for i in request_price:
            if i[0] != brand:
                list.append(float(i[1]) + (float(i[1]) * cls.find_rate(i[0]) / 100))
        for i in request_price:
            if i[0] == brand:
                brand_info = i
                list.append(float(i[1]) + (float(i[1]) * cls.find_rate(i[0]) / 100))
        if len(list) != 3:
            print()

        tr = tree.Node
        result = tr.calculate_best_move(list)

        cls.change_rate(((result[-1] * 100)/float(brand_info[1]))-100, brand)

    @classmethod
    def get_starting_fundamental_prices(cls):
        request = CloudRequest(brand=None, region="US East", os="Windows", cpu=1, ram=2, storage=256,
                               storage_type="SSD")
        vms = game.Jobs.search_vm(request, cloud_DB_VM)
        stos = game.Jobs.search_sto(request, cloud_DB_sto)
        request_price = []
        sum = 0

        for vm in vms:
            for sto in stos:
                if vm[0] == sto[0]:
                    request_price.append([vm[0], float(vm[5] + sto[4])])
        return request_price


    @classmethod
    def change_rate(cls, value, brand):
        if brand == "Google":
            cls.current_rate[0] = value
        elif brand == "Azure":
            cls.current_rate[1] = value
        elif brand == "Amazon":
            cls.current_rate[2] = value

    @classmethod
    def find_rate(cls, brand):
        if brand == "Google":
            return cls.current_rate[0]
        elif brand == "Azure":
            return cls.current_rate[1]
        elif brand == "Amazon":
            return cls.current_rate[2]
        else:
            pass

    @classmethod
    def update_rate(cls):
        cls.rate_history.append(cls.current_rate.copy())

    @classmethod
    def show_cloud_state(cls, cloud):
        first_provider = cloud.providers[0]
        second_provider = cloud.providers[1]
        third_provider = cloud.providers[2]

        # plt.ion()
        labels = 'Use', 'Empty'
        # FIRST BRAND CPU
        fig1, ax = plt.subplots(3, 3)
        empty = 0
        use = 0
        for i in first_provider.servers:
            use += i.cpu_in_service
        for i in first_provider.servers:
            empty += i.cpu - i.cpu_in_service
        explode = (0.1, 0)
        ax[0,0].pie([use, empty], explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax[0,0].axis('equal')
        ax[0,0].set_title(first_provider.brand + " CPU")

        # FIRST BRAND HDD
        empty = 0
        use = 0
        for i in first_provider.servers:
            use += i.hdd_storage_in_service
        for i in first_provider.servers:
            empty += i.hdd_storage - i.hdd_storage_in_service
        explode = (0.1, 0)
        ax[1,0].pie([use, empty], explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax[1,0].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax[1,0].set_title(first_provider.brand + " HDD")

        # FIRST BRAND SSD
        empty = 0
        use = 0
        for i in first_provider.servers:
            use += i.ssd_storage_in_service
        for i in first_provider.servers:
            empty += i.ssd_storage - i.ssd_storage_in_service
        explode = (0.1, 0)
        ax[2, 0].pie([use, empty], explode=explode, labels=labels, autopct='%1.1f%%',
                     shadow=True, startangle=90)
        ax[2, 0].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax[2, 0].set_title(first_provider.brand + " SSD")

        # SECOND BRAND CPU
        empty = 0
        use = 0
        for i in second_provider.servers:
            use += i.cpu_in_service
        for i in second_provider.servers:
            empty += i.cpu - i.cpu_in_service
        explode = (0.1, 0)
        ax[0,1].pie([use, empty], explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax[0,1].axis('equal')
        ax[0,1].set_title(second_provider.brand + " CPU")

        # SECOND BRAND HDD
        empty = 0
        use = 0
        for i in second_provider.servers:
            use += i.hdd_storage_in_service
        for i in second_provider.servers:
            empty += i.hdd_storage - i.hdd_storage_in_service
        explode = (0.1, 0)
        ax[1,1].pie([use, empty], explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax[1,1].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax[1,1].set_title(second_provider.brand + " HDD")

        # SECOND BRAND SSD
        empty = 0
        use = 0
        for i in second_provider.servers:
            use += i.ssd_storage_in_service
        for i in second_provider.servers:
            empty += i.ssd_storage - i.ssd_storage_in_service
        explode = (0.1, 0)
        ax[2, 1].pie([use, empty], explode=explode, labels=labels, autopct='%1.1f%%',
                     shadow=True, startangle=90)
        ax[2, 1].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax[2, 1].set_title(second_provider.brand + " SSD")

        # THIRD BRAND CPU
        empty = 0
        use = 0
        for i in third_provider.servers:
            use += i.cpu_in_service
        for i in third_provider.servers:
            empty += i.cpu - i.cpu_in_service
        explode = (0.1, 0)
        ax[0,2].pie([use, empty], explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax[0,2].axis('equal')
        ax[0,2].set_title(third_provider.brand + " CPU")

        # THIRD BRAND HDD
        empty = 0
        use = 0
        for i in third_provider.servers:
            use += i.hdd_storage_in_service
        for i in third_provider.servers:
            empty += i.hdd_storage - i.hdd_storage_in_service
        explode = (0.1, 0)
        ax[1, 2].pie([use, empty], explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax[1, 2].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax[1, 2].set_title(third_provider.brand + " HDD")

        # THIRD BRAND SSD
        empty = 0
        use = 0
        for i in third_provider.servers:
            use += i.ssd_storage_in_service
        for i in third_provider.servers:
            empty += i.ssd_storage - i.ssd_storage_in_service
        explode = (0.1, 0)
        ax[2, 2].pie([use, empty], explode=explode, labels=labels, autopct='%1.1f%%',
                     shadow=True, startangle=90)
        ax[2, 2].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax[2, 2].set_title(third_provider.brand + " SSD")

        plt.show()
