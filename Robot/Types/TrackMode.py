# TODO: Might be better as a universal import in a __init__.py file if possible for this submodule.
from enum import Enum


class TrackMode(Enum):
    BlueBlock = 0
    BlackLine = 1
    Shaving = 2
