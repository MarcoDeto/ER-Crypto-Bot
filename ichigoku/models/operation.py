class Operation:
   def __init__(self, _id, symbol, base, quote, isMarginTrade, isBuyAllowed, isSellAllowed, operation_number, cross, operation_type, time_frame):
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
