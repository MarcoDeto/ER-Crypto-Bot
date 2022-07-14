from models.enums import CycleType


def getTimeframesCycle(cycletype):
   match cycletype:
      case CycleType.Ottennale:
            return "3d"
      case CycleType.Quadriennale:
            return "3d"
      case CycleType.Biennale:
            return "1d"
      case CycleType.Annuale:
            return "1d"
      case CycleType.Semestrale:
            return "1d"
      case CycleType.Trimestrale:
            return "4h"
      case CycleType.Mensile:
            return "4h"
      case CycleType.Bisettimanale:
            return "2h"
      case CycleType.Settimanale:
            return "1h"
      case CycleType.FourDay:
            return "1h"
      case CycleType.TwoDay:
            return "1h"
      case CycleType.Day:
            return "30m"
      case CycleType.HalfDay:
            return "15m"
      case CycleType.SixH:
            return "5m"
      case CycleType.ThreeH:
            return "5m"


def getMinDays(cycletype):
   match cycletype:
      case CycleType.Ottennale:
         return 512
      case CycleType.Quadriennale:
         return 256
      case CycleType.Biennale:
         return 384
      case CycleType.Annuale:
            return 192
      case CycleType.Semestrale:
            return 96
      case CycleType.Trimestrale:
            return 288
      case CycleType.Mensile:
            return 144
      case CycleType.Bisettimanale:
            return 144
      case CycleType.Settimanale:
            return 144
      case CycleType.FourDay:
            return 72
      case CycleType.TwoDay:
            return 36
      case CycleType.Day:
            return 36 #se non valido usare "1h"
      case CycleType.HalfDay:
            return 36
      case CycleType.SixH:
            return 60
      case CycleType.ThreeH:
            return 24

from models.enums import CycleType


def getMaxDays(cycletype):
   match cycletype:
      case CycleType.Ottennale:
         return 896
      case CycleType.Quadriennale:
         return 448
      case CycleType.Biennale:
         return 672
      case CycleType.Annuale:
            return 336
      case CycleType.Semestrale:
            return 168
      case CycleType.Trimestrale:
            return 504
      case CycleType.Mensile:
            return 252
      case CycleType.Bisettimanale:
            return 252
      case CycleType.Settimanale:
            return 264
      case CycleType.FourDay:
            return 120
      case CycleType.TwoDay:
            return 66
      case CycleType.Day:
            return 66 
      case CycleType.HalfDay:
            return 68
      case CycleType.SixH:
            return 96
      case CycleType.ThreeH:
            return 60
