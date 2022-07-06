class Symbol:
   def __init__(self, symbol, base, quote, isMarginTrade, isBuyAllowed, isSellAllowed, operation_number):
               # _id, price, operation, cross, time_frame, ema_main, ema_second, CreateAT):
      # self._id = _id
      self.symbol = symbol
      self.base = base
      self.quote = quote
      self.isMarginTrade = isMarginTrade
      self.isBuyAllowed = isBuyAllowed
      self.isSellAllowed = isSellAllowed
      # self.price = price
      self.operation_number = operation_number
      # self.operation = operation
      # self.cross = cross
      # self.time_frame = time_frame
      # self.ema_main = ema_main
      # self.ema_second = ema_second
      # self.CreateAT = CreateAT