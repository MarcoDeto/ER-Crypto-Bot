from models.enums import CycleType

# i cicli di ritorno devono essere ribassiste
def getTimeframeCloseCheck(cycletype):
   match cycletype:
      case CycleType.Ottennale:
            return CycleType.Annuale
      case CycleType.Quadriennale:
            return CycleType.Semestrale
      case CycleType.Biennale:
            return CycleType.Trimestrale
      case CycleType.Annuale:
            return CycleType.Mensile
      case CycleType.Semestrale:
            return CycleType.Bisettimanale
      case CycleType.Trimestrale:
            return CycleType.Settimanale
      case CycleType.Mensile:
            return CycleType.FourDay
      case CycleType.Bisettimanale:
            return CycleType.TwoDay
      case CycleType.Settimanale:
            return CycleType.Day
      case CycleType.FourDay:
            return CycleType.HalfDay
      case CycleType.TwoDay:
            return CycleType.SixH
      case CycleType.Day:
            return CycleType.ThreeH



# i cicli di ritorno devono essere rialzista
def getTimeframeOpenCheck(cycletype):
   match cycletype:
      case CycleType.Ottennale:
            return CycleType.Biennale
      case CycleType.Quadriennale:
            return CycleType.Annuale
      case CycleType.Biennale:
            return CycleType.Semestrale
      case CycleType.Annuale:
            return CycleType.Trimestrale
      case CycleType.Semestrale:
            return CycleType.Mensile
      case CycleType.Trimestrale:
            return CycleType.Bisettimanale
      case CycleType.Mensile:
            return CycleType.Settimanale
      case CycleType.Bisettimanale:
            return CycleType.FourDay
      case CycleType.Settimanale:
            return CycleType.TwoDay
      case CycleType.FourDay:
            return CycleType.Day
      case CycleType.TwoDay:
            return CycleType.HalfDay
      case CycleType.Day:
            return CycleType.SixH
