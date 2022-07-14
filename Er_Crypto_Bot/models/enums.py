from enum import Enum
class Status(Enum):
   OPEN = 1
   CLOSE = 2

class CrossType(Enum):
   LONG = 1
   SHORT = 2

class CycleType(Enum):
   Ottennale = 1
   Quadriennale = 2
   Biennale = 3
   Annuale = 4
   Semestrale = 5
   Trimestrale = 6
   Mensile = 7
   Bisettimanale = 8
   Settimanale = 9
   FourDay = 10
   TwoDay = 11
   Day = 12
   HalfDay = 13
   SixH = 14
   ThreeH = 15


