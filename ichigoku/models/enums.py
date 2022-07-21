from enum import Enum
class Status(Enum):
   OPEN = 1
   CLOSE = 2

class CrossType(Enum):
   LONG = 1
   SHORT = 2

class RSIType(Enum):
   OVERBOUGHT = 1
   OVERSOLD = 2