# TODO: Might be better as a universal import in a __init__.py file if possible for this submodule.
from enum import Enum


class TrackMode(Enum):
    none = 0
    BlueBlock = 1
    Autonomous = 2
