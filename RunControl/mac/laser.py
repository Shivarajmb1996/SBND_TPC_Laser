__author__ = 'matthias'

from devices.laser import *

laser = Laser(0)
laser.color = False
laser.comTimeout = 0.5
laser.com_init()

laser.getStatus()
print("Starting the Laser within 5 second")
time.sleep(5)
laser.start()
print("Wait for 15 minute")
time.sleep(900)
print("Now you are good to go....")

