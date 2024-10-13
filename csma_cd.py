import random

class Channel:
    def __init__(self, bandwidth, Tp):
        self.bandwidth = bandwidth
        self.Tp = Tp
        self.busy = False
        self.current_station = None
        self.busy_delay = 0
        self.finish_delay = 0

class Station:
    def __init__(self, ID, frame_size, channel, p):
        self.ID = ID
        self.frame_size = frame_size
        self.channel = channel
        self.p = p
        self.ready = True
        self.waiting_period = 0
        self.drop_period = 0
        self.k = 0
        self.jamming = False
        self.count = 0
        self.sending = False

    def exponential_backoff(self):
        if self.k < 15:
            self.k += 1
            self.waiting_period = random.randint(0, 2 ** self.k - 1)
        else:
            self.k = 0
            self.drop_period = 5

    def p_persistence(self):
        if self.sending:
            return False
        elif self.drop_period > 0:
            self.drop_period -= 1
            return False
        elif self.waiting_period == 0 and not self.channel.busy:
            if random.random() < self.p:
                return True
            else:
                return False
        elif self.waiting_period > 0:
            self.waiting_period -= 1
            return False
        else:
            self.exponential_backoff()

    def interrupt(self):
        self.channel.busy_delay = 0
        self.channel.current_station = None
        self.jamming = True
        self.sending = False
        self.exponential_backoff()

def simulate(stations, channel, time):
    time_slots = time * 1000

    with open('log.txt', 'w') as log:
        while time_slots > 0:
            jamming = False
            for _, station in stations.items():
                if station.jamming:
                    jamming = True
                    log.write(f"Jamming by {station.ID}\n")
                    station.jamming = False
                    break

            if jamming:
                time_slots-=1
                continue

            if not channel.busy:
                if channel.busy_delay > 0:
                    channel.busy_delay -= 1
                if channel.finish_delay > 0:
                    channel.finish_delay -= 1

                if channel.busy_delay == 0 and channel.current_station:
                    channel.busy = True
                    log.write("Busy bit enabled")

                ready = []
                for _, station in stations.items():
                    if station.p_persistence():
                        ready.append(station)

                if channel.current_station is None and len(ready) == 1:
                    channel.busy_delay = channel.Tp
                    channel.finish_delay = ready[0].frame_size // channel.bandwidth
                    channel.current_station = ready[0].ID
                    ready[0].sending = True
                    log.write(f"{ready[0].ID} started sending\n")

                elif channel.current_station is not None and ready:
                    if channel.current_station:
                        log.write(f"{channel.current_station} interrupted. ")
                        stations[channel.current_station].interrupt()
                    log.write("Exponential backoffs performed by: ")
                    for station in ready:
                        station.exponential_backoff()
                        log.write(f"{station.ID} ")
                    log.write("\n")
                else:
                    log.write(".\n")
            else:
                if channel.finish_delay > 0:
                    channel.finish_delay -= 1

                if channel.finish_delay == 0:
                    stations[channel.current_station].count += 1
                    stations[channel.current_station].sending = False
                    stations[channel.current_station].drop_period = 1
                    channel.current_station = None
                    channel.busy = False
                    log.write("Transmission successful. Busy bit disabled\n")
                else:
                    log.write(".\n")

            time_slots -= 1

channel = Channel(bandwidth=1000, Tp=5)
stations = {
    "A": Station(ID="A", frame_size=12000, channel=channel, p=0.5),
    "B": Station(ID="B", frame_size=16000, channel=channel, p=0.7),
    "C": Station(ID="C", frame_size=11000, channel=channel, p=0.3)
}

simulate(stations, channel, time=5)

for id, station in stations.items():
    print(f'{id} {station.count}')