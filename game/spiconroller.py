import spidev
import time

spi = spidev.SpiDev()
spi.mode = 0b00
spi.open(0,0)
spi.max_speed_hz = 50000
value = 0
to_send = [value]
try:
	while True:
		resp = spi.xfer2(to_send)
		print("sent:")
		print(value)
		value += 1
		to_send = [value]
		print("response:")
		respString = " ".join(str(x) for x in resp)
		print(respString + " | " + "{0:b}".format(int(float(respString))))
		time.sleep(0.5)
	#end while
except KeyboardInterrupt:
	print("closing on keyboard interrupt")
	spi.close()
#end try
