import numpy as np
from datetime import datetime
from threading import Timer
from threading import Lock
import redis_connector as connector
import time
import plotext as plt
import os

###connection parameters###
host = "127.0.0.1"
port = 80
###end - connection parameters###

### definitions
mean_velocity_f = 0.32  # mean velocity of the rolled material exiting the process in m/s
mean_velocity_r = 0.3  # max velocity of the roll in m/s
stream_name = "mubea_trb"

###global list of measurements
measurements = []

client = connector.connect()
with client:
    client.ping()

class Measurement:
    def __init__(self, f: float, r: float):
        self.velocity_f = f
        self.velocity_r = r
        self.date = datetime.now()

        global measurements
        lock = Lock()
        with lock:
            measurements.append(self)
            self.storeInRedis()
    def __str__(self):
        return "Measurement taken " + self.date.strftime("%m/%d/%Y, %H:%M:%S:%f") + " - velocity_f: " + str(
            self.velocity_f) + " - velocity_r: " + str(self.velocity_r)
    def __repr__(self):
        return str(self)

    def storeInRedis(self):
        with client:
            client.xadd(stream_name, {"date": str(self.date), "velocity_f": str(self.velocity_f),  "velocity_r": str(self.velocity_r)})

def simulateMeasurement():
    num_r = np.random.default_rng().normal(mean_velocity_r, 0.01, size=None)
    num_f = np.random.uniform(low=max(mean_velocity_f, num_r), high=min(mean_velocity_f, num_r), size=None)
    m = Measurement(num_f, num_r)
    return m


def simulateRuns(runs: int, delay_ms: int):

    for i in range(runs):
        t = Timer(delay_ms/1000, simulateMeasurement, args=())
        t.start()
        t.join()


def viewRuns(runs: int):
    labels = []
    velocities_f = []
    velocities_r = []
    slip = []

    with client:
        l = client.xlen(stream_name)
        if l > 0:
            values = client.xrevrange(stream_name, min='-', max='+', count=min(l, runs)) #getting the last elements from stream
            values.reverse() # reversing for better plot
            for v in values:
                id, data = v

                labels.append(datetime.strptime(data.get('date'), "%Y-%m-%d %H:%M:%S.%f"))
                velocities_f.append(float(data.get('velocity_f')))
                velocities_r.append(float(data.get('velocity_r')))

                s = 1 if float(data.get('velocity_f'))<float(data.get('velocity_r')) else 0
                slip.append(s)

            title = 'Last Runs'
            os.system('cls' if os.name == 'nt' else 'clear')
            plt.clt()
            plt.clf()
            #

            dates = plt.datetimes_to_string(labels)
            plt.plot(velocities_f, label="f",  yside = "left")
            plt.plot(velocities_r, label="r",  yside = "left")
            plt.scatter(slip, label="slip",  yside = "right")

            #
            plt.interactive(True)
            plt.show()

            time.sleep(1)


test = Timer(1, simulateRuns, args=(500, 200))
test.start()

try:
    while True:
        viewRuns(100)

except KeyboardInterrupt:
    pass



