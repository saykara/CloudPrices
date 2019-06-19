import random
import cloudServer
import parameters
import game
import copy


class CloudRequest:
    def __init__(self, brand, region, os, cpu, ram, storage_type, storage):
        self.brand = brand
        self.region = region
        self.os = os
        self.cpu = cpu
        self.ram = ram
        self.storage_type = storage_type
        self.storage = storage


class Simulator:
    successful = 0
    erase_count = 0
    vm = 0
    sto = 0
    cum = 0
    out_cum = 0
    out_vm = 0
    out_sto = 0
    fail = 0

    def __init__(self):
        self.fel = []
        self.cloud = None

    class Event:
        def __init__(self, event_time, detail):
            self.event_time = event_time
            self.detail = detail

        def process(self, fel, cloud, clock):
            raise NotImplementedError

    class CustomerArrivalEvent(Event):
        def __init__(self, event_time, detail):
            super().__init__(event_time, detail)

        def process(self, fel, cloud, clock):
            result, is_enough_vm, is_enough_storage = game.Jobs.customer_arrival_job(cloud=cloud, request=self.detail)
            if not result:
                if not is_enough_storage and not is_enough_vm:
                    Simulator.cum += 1
                    fel.append(Simulator.OutsourceCloud(event_time=clock, detail=self.detail))
                elif not is_enough_vm:
                    Simulator.vm += 1
                    fel.append(Simulator.OutsourceVM(event_time=clock, detail=self.detail))
                elif not is_enough_storage:
                    Simulator.sto += 1
                    fel.append(Simulator.OutsourceStorage(event_time=clock, detail=self.detail))
            else:
                fel.append(Simulator.CloudExpiredEvent(event_time=clock + Simulator.cloud_expired_time(),
                                                       detail=self.detail))
                Simulator.successful += 1
            fel.append(Simulator.CustomerArrivalEvent(event_time=clock + Simulator.customer_inter_arrival_time(),
                                                      detail=Simulator.create_request_automatically()))

    class CloudExpiredEvent(Event):
        def __init__(self, event_time, detail):
            super().__init__(event_time, detail)

        def process(self, fel, cloud, clock):
            game.Jobs.erase_server_job(cloud=cloud, request=self.detail)
            Simulator.erase_count += 1

    class OutsourceCloud(Event):
        def __init__(self, event_time, detail):
            super().__init__(event_time, detail)

        def process(self, fel, cloud, clock):
            new_request = copy.copy(self.detail)
            new_request.storage = 0
            self.detail.ram = 0
            self.detail.cpu = 0

            updated_request_vm = game.Jobs.find_provider_job(cloud, new_request)
            updated_request_sto = game.Jobs.find_provider_job(cloud, self.detail)

            if updated_request_vm:
                time = clock + Simulator.cloud_expired_time()

                result, is_enough_vm, is_enough_storage = game.Jobs.customer_arrival_job(cloud=cloud,
                                                                                         request=updated_request_vm)
                if result:
                    fel.append(Simulator.CloudExpiredEvent(event_time=time, detail=updated_request_vm))
            if updated_request_sto:
                result, is_enough_vm, is_enough_storage = game.Jobs.customer_arrival_job(cloud=cloud,
                                                                                         request=updated_request_sto)
                if result:
                    fel.append(Simulator.CloudExpiredEvent(event_time=time, detail=updated_request_sto))
            Simulator.out_cum += 1
            if not updated_request_vm and not updated_request_sto:
                Simulator.fail += 1

    class OutsourceVM(Event):
        def __init__(self, event_time, detail):
            super().__init__(event_time, detail)

        def process(self, fel, cloud, clock):
            new_request = copy.copy(self.detail)
            new_request.storage = 0
            self.detail.ram = 0
            self.detail.cpu = 0

            updated_request = game.Jobs.find_provider_job(cloud, new_request)

            if updated_request:
                time = clock + Simulator.cloud_expired_time()

                result, is_enough_vm, is_enough_storage = game.Jobs.customer_arrival_job(cloud=cloud, request=self.detail)
                if result:
                    fel.append(Simulator.CloudExpiredEvent(event_time=time, detail=self.detail))

                result, is_enough_vm, is_enough_storage = game.Jobs.customer_arrival_job(cloud=cloud, request=updated_request)
                if result:
                    fel.append(Simulator.CloudExpiredEvent(event_time=time, detail=updated_request))
                Simulator.out_vm += 1
            else:
                Simulator.fail += 1

    class OutsourceStorage(Event):
        def __init__(self, event_time, detail):
            super().__init__(event_time, detail)

        def process(self, fel, cloud, clock):
            new_request = copy.copy(self.detail)
            new_request.cpu = 0
            new_request.ram = 0
            self.detail.storage = 0

            updated_request = game.Jobs.find_provider_job(cloud, new_request)

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
                Simulator.out_sto += 1
            else:
                Simulator.fail += 1

    @classmethod
    def fel_key(cls, event):
        return event.event_time

    def create_cloud_randomly(self):
        self.cloud = cloudServer.create_clouds_randomly()

    def simulation(self, range):
        clock = 0
        self.create_cloud_randomly()
        self.fel.append(self.CustomerArrivalEvent(event_time=clock, detail=Simulator.create_request_automatically()))
        while self.fel and self.successful + self.cum + self.vm + self.sto < range:
            self.fel.sort(key=self.fel_key)
            next_event = self.fel[0]
            del self.fel[0]
            clock = next_event.event_time
            next_event.process(fel=self.fel, clock=clock, cloud=self.cloud)
        print("Successful without Outsource: ", self.successful)
        print("Successful with Outsource: ", range - self.fail)
        print("Unsuccessful without Outsource: ", self.vm + self.sto + self.cum)
        print("Unsuccessful with Outsource: ", self.fail)
        print("Erase: ", self.erase_count)
        print("Lack of VM: ", self.vm)
        print("Lack of Storage: ", self.sto)
        print("Lack of Both: ", self.cum)
        print("Outsource of VM: ", self.out_vm)
        print("Outsource of Storage: ", self.out_sto)
        print("Outsource of Both: ", self.out_cum)

    @classmethod
    def customer_inter_arrival_time(cls):
        return random.uniform(0, 1)

    @classmethod
    def cloud_expired_time(cls):
        # return np.random.normal(50, 20)
        return random.uniform(30, 60)

    @classmethod
    def create_request_automatically(cls):
        par = parameters.CloudParameters()
        cpu = random.choice(par.cpu)
        ram = random.choice(par.ram[str(cpu)])
        return CloudRequest(brand=random.choice(par.brand), os=random.choice(par.os), region=random.choice(par.region),
                            cpu=cpu, ram=ram, storage_type=random.choice(par.s_type),
                            storage=random.choice(par.s_capacity))

    @classmethod
    def sim(cls):
        sim = Simulator()
        sim.simulation(20000)
