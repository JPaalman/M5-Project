import spidev
import time
from threading import Thread

run = False
data = None
FREQ = 60


def run():
    t = Thread(target=runThread)
    t.start()


def runThread():
    start = time.time()
    global run
    run = True
    print("1")
    spi = spidev.SpiDev()
    spi.mode = 0b00
    print("2")
    spi.open(0, 0)
    print("3")
    spi.max_speed_hz = 50000
    value = 0
    to_send = [value]
    while run:
        print(str(run))
        resp = spi.xfer2(to_send)
        global data
        cpy = str(resp)
        data = process(cpy)
        print("sent:")
        print(value)
        value += 1
        to_send = [value]
        print("response:")
        respString = " ".join(str(x) for x in resp)
        print(respString + " | " + "{0:b}".format(int(float(respString))))
        print("Timediff: " + str(time.time() - start))
        time.sleep(1 / (FREQ - (time.time() - start)))
    spi.close()


def read():
    if run:
        return data
    print("ERROR: Tried to read FPGA value while the controller is not running")
    return None


def process(data):
    # Maybe do something with the data
    return data


def stop():
    global run
    run = False


run()
time.sleep(20)
