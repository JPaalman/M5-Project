import wiringpi
import time
from threading import Thread

run = False
data = None
FREQ = 60


def run():
    t = Thread(target=runThread)
    t.start()


def runThread():
    global run
    run = True
    SPIchannel = 0  # SPI Channel (CE0)
    SPIspeed = 1000000  # Clock Speed in Hz
    wiringpi.wiringPiSetupGpio()
    wiringpi.wiringPiSPISetup(SPIchannel, SPIspeed)
    value = 0
    to_send = bytes([value])
    while run:
        start = time.time()
        print(str(run))
        resp = wiringpi.wiringPiSPIDataRW(SPIchannel, to_send)
        global data
        cpy = str(resp)
        data = process(cpy)
        print("sent:")
        print(value)
        # value += 1
        # to_send = [value]
        print("response:")
        print(str(resp))
        print("Timediff: " + str(time.time() - start))
        time.sleep(1 / (FREQ - (time.time() - start)))


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
