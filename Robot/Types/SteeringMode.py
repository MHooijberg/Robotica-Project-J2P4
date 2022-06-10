from enum import Enum


class SteeringMode(Enum):
    # Old school style, forwards / backwards and turn. but not a the same time.
    static = 0
    # You can only drive and turn.
    dynamic = 1
    # You can drive and turn at the same time. but at max steering you will turn 100% around axis
    smooth = 2
