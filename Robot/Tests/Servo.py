from ax12_v3_modified import Ax12

servo = Ax12()
servo.move(23, 10)
print(servo.readVoltage(23))
# print(servo.ping(23))
#servo.learnServos(22, 23, True)
#servo.move(23, 960)
