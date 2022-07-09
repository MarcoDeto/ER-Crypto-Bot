class Operation:
   def __init__(self, _id, symbol, base, quote, isMarginTrade, isBuyAllowed, isSellAllowed, operation_number, cross, operation_type, second_ema, time_frame):
               # _id, price, operation, cross, time_frame, ema_main, ema_second, CreateAT): 
      self._id = _id
      self.symbol = symbol
      self.base = base
      self.quote = quote
      self.isMarginTrade = isMarginTrade
      self.isBuyAllowed = isBuyAllowed
      self.isSellAllowed = isSellAllowed
      self.operation_number = operation_number
      self.cross = cross
      self.operation_type = operation_type
      self.time_frame = time_frame
      self.ema_second = second_ema
