from enum import Enum

_K = 1000
class ETimeFormat(Enum):
    Nanosec = 1
    Microsec = Nanosec * _K
    Milisec = Microsec * _K
    Sec = Milisec * _K

def time_conversion(time: int | float, _from: ETimeFormat, to: ETimeFormat):
    scalar = _from.value / to.value if _from.value > to.value else float(_from.value) / float(to.value)
    return time * scalar