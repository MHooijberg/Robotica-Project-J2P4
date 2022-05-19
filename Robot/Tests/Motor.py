import Motor
import time


def MotorTest():
    mdd3a = Motor.mdd3aDriver(12, 18, 13, 19)
    while True:
        mdd3a.forward(100)
        time.sleep(3)
        mdd3a.backward(100)
        time.sleep(3)
        mdd3a.stop()
        time.sleep(3)


# TODO: Define how we test, now this code will be executed after importing (if I'm not mistaken).
MotorTest()
