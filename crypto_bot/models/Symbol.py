class Symbol:
   def __init__(self, symbol, base, quote, isMarginTrade, isBuyAllowed, isSellAllowed):
      self.symbol = symbol
      self.base = base
      self.quote = quote
      self.isMarginTrade = isMarginTrade
      self.isBuyAllowed = isBuyAllowed
      self.isSellAllowed = isSellAllowed