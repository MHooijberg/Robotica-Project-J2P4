import imp
import RPi.GPIO as GPIO
from serial import Serial
from time import sleep
from Types.Component import Component


class SerialDriver:

    def __init__(self, pin, swithDelay, bautRateDisplay, bautRateServo, startDevice):
        self.Pin = pin
        self.SwithDelay = swithDelay
        self.BautRateDisplay = bautRateDisplay
        self.BautRateServo = bautRateServo
        if startDevice == Component.Display:
            self.currentDevice = startDevice
            startBaudRate = bautRateDisplay
            self.Switch(Component.Display)
        elif startDevice == Component.Servo:
            self.currentDevice = startDevice
            startBaudRate = bautRateServo
            self.Switch(Component.Servo)
        self.SerialPort = Serial(
            "/dev/serial0", baudrate=startBaudRate, timeout=0.001)

    def Switch(self, device):
        if (self.currentDevice != device):
            if device == Component.Display:
                GPIO.output(self.Pin, GPIO.HIGH)
            elif device == Component.Display:
                GPIO.output(self.Pin, GPIO.LOW)
            self.currentDevice = device
            sleep(self.SwitchDelay)

    def flushInput(self, device):
        if (self.currentDevice != device):
            self.Switch(device)
        self.SerialPort.flushInput()

    def write(self, data, device):
        if (self.currentDevice != device):
            self.Switch(device)
        self.SerialPort.write(data)

    def read(self, device):
        if (self.currentDevice != device):
            self.Switch(device)
        return self.SerialPort.read()
