import serial

class Attenuator:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600):
        self.com = serial.Serial(port=port, baudrate=baudrate, timeout=1)
        if not self.com.is_open:
            self.com.open()

    def enableMotor(self):
        if self.com.is_open:
            self.com.write(b'en 1\r')
        else:
            raise serial.serialutil.PortNotOpenError("Port is not open")

# Usage
att = Attenuator(port='/dev/ttyUSB0')
att.enableMotor()
print(" Testing")


