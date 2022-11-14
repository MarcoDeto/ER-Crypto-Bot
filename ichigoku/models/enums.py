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

class Trend(Enum):
   UPTREND = 1
   DOWNTREND = 2
   
class GokuTrend(Enum):
   GOKUVERDE = 0
   GOKUROSSO = 1