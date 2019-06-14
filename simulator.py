import random
import cloudServer
import parameters
import game


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
            result = game.Jobs.customer_arrival_job(cloud=cloud, request=self.detail)
            if not result:
                fel.append(Simulator.CloudExpiredEvent(event_time=clock + Simulator.cloud_expired_time(), detail=self.detail))
                print("Time:", clock, "Event:", "Server is not available.")
            else:
                print("Time:", clock, "Event:", "Server is given.")
            fel.append(Simulator.CustomerArrivalEvent(event_time=clock + Simulator.customer_inter_arrival_time(),
                                                      detail=Simulator.create_request_automatically()))

    class CloudProviderFillUp(Event):
        def __init__(self, event_time, detail):
            super().__init__(event_time, detail)

        def process(self, fel, cloud, clock):
            raise NotImplementedError

    class CloudExpiredEvent(Event):
        def __init__(self, event_time, detail):
            super().__init__(event_time, detail)

        def process(self, fel, cloud, clock):
            game.Jobs.erase_server_job(cloud=cloud, request=self.detail)
            print("Time:", clock, "Event:", "Server erased.")

    class OutsourceCloud(Event):
        def __init__(self, event_time, detail):
            super().__init__(event_time, detail)

        def process(self, fel, cloud, clock):
            raise NotImplementedError

    @classmethod
    def fel_key(cls, event):
        return event.event_time

    def create_cloud_randomly(self):
        self.cloud = cloudServer.create_clouds_randomly()

    def simulation(self):
        clock = 0
        self.create_cloud_randomly()
        self.fel.append(self.CustomerArrivalEvent(event_time=clock, detail=Simulator.create_request_automatically()))
        while self.fel and clock<1000:
            self.fel.sort(key=self.fel_key)
            next_event = self.fel[0]
            del self.fel[0]
            clock = next_event.event_time
            next_event.process(fel=self.fel, clock=clock, cloud=self.cloud)

    @classmethod
    def customer_inter_arrival_time(cls):
        return random.uniform(0, 3)

    @classmethod
    def cloud_expired_time(cls):
        return random.uniform(15, 60)

    @classmethod
    def create_request_automatically(cls):
        par = parameters.CloudParameters()
        return CloudRequest(brand=random.choice(par.brand), os=random.choice(par.os), region=random.choice(par.region),
                            cpu=random.choice(par.cpu), ram=random.choice(par.ram), storage_type=random.choice(par.s_type),
                            storage=random.choice(par.s_capacity))


if __name__ == "__main__":
    sim = Simulator()
    sim.simulation()