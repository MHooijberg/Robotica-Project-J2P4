from enum import Enum

# TODO: The setting to steer around middle point might not be this this should relate more
#       To how the steering from the joystick is seen by the robot.
class SteeringMode(Enum):
    Static = 0 # Old school style, forwards / backwards and turn. but not a the same time.
    Dynamic = 1 # You can only drive and turn.
    Smooth = 2 # You can drive and turn at the same time. but at max steering you will turn 100% around axis