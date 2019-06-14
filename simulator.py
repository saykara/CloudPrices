import random

class simulator:
    def __init__(self):
        self.fel = []

    class Event:
        def __init__(self, event_time):
            self.event_time = event_time

        def process(self, fel, clock):
            raise NotImplementedError

    class CustomerArrivalEvent(Event):
        def __init__(self, event_time):
            super().__init__(event_time)

        def process(self, fel, clock):
            raise NotImplementedError

    class CloudProviderFillUp(Event):
        def __init__(self, event_time):
            super().__init__(event_time)

        def process(self, fel, clock):
            raise NotImplementedError

    class OutsourceCloud(Event):
        def __init__(self, event_time):
            super().__init__(event_time)

        def process(self, fel, clock):
            raise NotImplementedError


    @classmethod
    def fel_key(cls, event):
        return event.event_time

    def simulation(self):
        clock = 0

        while self.fel:
            self.fel.sort(key=self.fel_key)
            next_event = self.fel[0]
            del self.fel[0]
            clock = next_event.event_time
            next_event.process(fel=self.fel, clock=clock)

    @classmethod
    def customer_inter_arrival_time(cls):
        return random.uniform(0, 3)

    @classmethod
    def cloud_expired_time(cls):
        return random.uniform(15, 60)

