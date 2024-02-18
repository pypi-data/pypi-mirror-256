from enum import Enum


class Status(Enum):
    WA = "\033[31mWA\033[0m"
    PA = "\033[34mPA\033[0m"
    TA = "\033[31mTA\033[0m"
