# return minimum amount in for a given amount out
def getAmountIn(amountOut: int, reserveIn: int, reserveOut: int) -> int:
  if not amountOut > 0 or not reserveIn * reserveOut > 0:
      print('[!] getAmountIn() err: Insufficient quantity')
    return 0
  else:
    numerator = (reserveIn * amountOut) * 1000
    denominator = (reserveOut - amountOut) * 997
    amountIn = (numerator / denominator) + 1
    return int(amountIn)

# return float multiplier for a given int between 0-100
def _get_multiplier(percent: float) -> float:
  if percent < 0 or percent > 100:
    print('[!] _get_multiplier() err: Percentage out of range:', percent)
    return 0
  else:
    return float(percent / 100)

# return a percent amount of 'supply'
def get_percent(percent: int, supply: int) -> int:
  return round(_get_multiplier(percent) * supply)

# return eth needed to buy percent of a tokens supply
def quote(
  percent: int,
  supply: int,
  eth_reserve: int,
  token_reserve: int
) -> int:
  amount = get_percent(percent, supply)
  if amount > token_reserve:
    print('[!] quote() err: AmountOut exceeds pool reserve, try an aggregator')
    return 0
  else:
    return getAmountIn(amount, eth_reserve, token_reserve)
