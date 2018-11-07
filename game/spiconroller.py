import time
from threading import Thread
from pynput.keyboard import Key, Controller
import wiringpi


class SPIController:
    FREQ = 48

    def __init__(self):
        self.data = [0,0]
        self.run = False
        self.keyboard = Controller()

        self.left = False
        self.right = False
        self.space = False

        self.rms = 0

    def start(self):
        t = Thread(target=self.runThread)
        t.start()

    def runThread(self):
        print("started spi controller")
        self.run = True
        SPIchannel = 0  # SPI Channel (CE0)
        SPIspeed = 1000000  # Clock Speed in Hz
        wiringpi.wiringPiSetupGpio()
        wiringpi.wiringPiSPISetup(SPIchannel, SPIspeed)
        value = 1
        to_send = bytes([value])
        while self.run:
            start = time.time()

            print(str(self.run))
            self.data[0] = int(wiringpi.wiringPiSPIDataRW(SPIchannel, to_send)[1])
            self.data[1] = int(wiringpi.wiringPiSPIDataRW(SPIchannel, to_send)[1])
            print("sent:")
            print(value)
            # value += 1
            # to_send = [value]
            print("response:")
            print(str(self.data))
            print("Timediff: " + str(time.time() - start))
            self.split(self.data)
            time.sleep(1 / (self.FREQ - (time.time() - start)) + 0.01)
        print("stopped spi controller")

    def split(self, data):
        # byte 1: button1, button2, RMS (6bit)
        # byte 2: frequency

        byte1 = self.bitfield(data[0])
        print(str(byte1))
        
        # split bit for button 1
        tmp = byte1[0]
        
        if tmp == 1:
            button1 = 0
        else:
            button1 = 1
        
        # split bit for button 2
        tmp = byte1[1]
        
        if tmp == 1:
            button2 = 0
        else:
            button2 = 1
        
        # split bits for RMS
        rms = self.getint(byte1[-6:])

        self.rms = rms

        if button2 == 1:
            if not self.right:
                self.keyboard.press(Key.right)
                self.right = True
        elif self.right:
            self.keyboard.release(Key.right)
            self.right = False

        if button1:
            if not self.left:
                self.keyboard.press(Key.left)
                self.left = True
        elif self.left:
            self.keyboard.release(Key.left)
            self.left = False

    def read(self):
        if self.run:
            return self.data
        print("ERROR: Tried to read FPGA value while the controller is not running")
        return None

    def process(self, data):
        # Maybe do something with the data
        return data

    def stop(self):
        self.run = False
        self.keyboard.release(Key.right)
        self.keyboard.release(Key.left)
        self.keyboard.release(Key.space)

    def bitfield(self, n):
        ls = [1 if digit == '1' else 0 for digit in bin(n)[2:]]
        while len(ls) < 8:
            ls.append(0)
        return ls

    def getint(self, bitfield):
        out = 0
        for bit in bitfield:
            out = (out << 1) | bit
        return out
