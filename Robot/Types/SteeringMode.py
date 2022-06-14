from enum import Enum


class SteeringMode(Enum):
    Static = 0 # Old school style, forwards / backwards and turn. but not a the same time.
    Dynamic = 1 # You can only drive and turn.
    Smooth = 2 # You can drive and turn at the same time. but at max steering you will turn 100% around axis