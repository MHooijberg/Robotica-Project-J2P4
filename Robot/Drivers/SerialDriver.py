import imp
import RPi.GPIO as GPIO
from serial import Serial
from time import sleep
from Types.Component import Component


class SerialDriver:
    Pin = 24
    SwithDelay = 0.0001
    BautRateDisplay = 115200
    BautRateServo = 1000000
    currentDevice = Component.Display

    SerialPort = Serial(
        "/dev/serial0", baudrate=BautRateDisplay, timeout=0.001)

    @staticmethod
    def Switch(device):
        if (SerialDriver.currentDevice != device):
            if device == Component.Display:
                SerialDriver.SerialPort.bautrate = SerialDriver.BautRateDisplay
                GPIO.output(SerialDriver.Pin, GPIO.HIGH)
            elif device == Component.Servo:
                SerialDriver.SerialPort.bautrate = SerialDriver.BautRateServo
                GPIO.output(SerialDriver.Pin, GPIO.LOW)
            SerialDriver.currentDevice = device
            sleep(SerialDriver.SwitchDelay)

    @staticmethod
    def flushInput(device):
        SerialDriver.Switch(device)
        SerialDriver.SerialPort.flushInput()

    @staticmethod
    def write(data, device):
        SerialDriver.Switch(device)
        SerialDriver.SerialPort.write(data)

    @staticmethod
    def read(bytesToRead, device):
        SerialDriver.Switch(device)
        return SerialDriver.SerialPort.read(bytesToRead)
