from enum import Enum


class LifeStatus(Enum):
    ST_EMPTY = 0
    ST_DEAD = 1
    ST_BORN = 2
    ST_LIFE = 3


class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    TOP = 3
    BOTTOM = 4
