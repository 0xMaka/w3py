# __ Imports and initialisations ______________________________________________
from x import con
import asyncio
from os import getenv
from dotenv import load_dotenv
from time import time

load_dotenv()
w3 = con('POLYGON')

# __ Configuration ____________________________________________________________
# @notice where to store receipts
LOGS = 'logs/receipts.log'
# @notice import account
EOA = '<INSERTADDRESS>'
KEY = getenv('RANGE_KEY')
# @notice hardcode decimals
RES0_DEC = 18
RES1_DEC = 6
# @notice target pool (WMATIC -> USDC)
PAIR_ADDRESS = '0x6e7a5FAFcec6BB1e78bAE2A1F0B612012BF14827'
WMATIC = '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270'
USDC = '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174'
# @notice for now: Quickswap router
ROUTER_ADDRESS = '0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff'
# @dev if there is a delay, how long.
POLL_DELAY = 2
# @notice position size in USDC
SIZE = 20000000
# @notice buy n sell ranges
supply_zone = 0.79
demand_zone = 0.74
stop_loss = 0.697
# @notice volatile settings
cached_nonce = w3.eth.get_transaction_count(EOA)
  
# __ Helpers __________________________________________________________________
def fetch_abi(_file: str) -> str:
  with open(f'abi/{_file}') as f:
    abi = f.read().strip()
  return abi

def c_init(_addr: str, _abi: str) -> object:
  return w3.eth.contract(address=_addr, abi=_abi)

def get_reserves(_pair: object) -> (int, int, int):
  return _pair.functions.getReserves().call()

async def poll_reserves(_pair: object) -> list:
  res0, res1, stamp = get_reserves(_pair)
  await asyncio.sleep(POLL_DELAY)
  return [res0, res1, stamp]

# __ Filler functions _________________________________________________________
def from_wei(_n: int, _dec: int) -> float:
  return _n / 10 ** _dec

def to_wei(_n: int, _dec: int) -> int:
  return int(_n * 10 ** _dec)

def calcSlippage(_slippage: float, _amount: int) -> int:
  return int(_slippage / 100 * _amount)

def dline() -> int:
  return round(time()) + (60 * 5)

def getAmountOut(amountIn: int, reserveIn: int, reserveOut: int) -> int:
  amountInWithFee = amountIn * 997
  numerator = amountInWithFee * reserveOut
  denominator = (reserveIn * 1000) + amountInWithFee
  amountOut = numerator / denominator
  return int(amountOut)

def getAmountIn(amountOut: int, reserveIn: int, reserveOut: int) -> int:
  numerator = reserveIn * (amountOut * 1000)
  denominator = reserveOut - (amountOut * 997)
  amountIn = (numerator / denominator) + 1
  return int(amountIn)  

tx = {        
        'chainId': 137,
        'type': '0x2',  
        'from': EOA, 
        'value': 0, 
        'gas': 200000,
        'maxFeePerGas': 35000000000, 
        'maxPriorityFeePerGas': 35000000000, 
        'nonce': cached_nonce
}

def from_exact(
  _router: object, 
  _amount_in: int, 
  _amount_out_min: int,
  _token_in: str,
  _token_out: str
):
  return _router.functions.swapExactTokensForTokens(
    _amount_in,
    _amount_out_min,
    [_token_in, _token_out],
    EOA,
    dline(),
  ).buildTransaction(tx)

def to_exact(
  _router: object,
  _amount_out: int,
  _amount_in_max: int,
  _token_in: str,
  _token_out: str
):
  return _router.functions.swapTokensForExactTokens(
    _amount_out,
    _amount_in_max,
    [_token_in, _token_out],
    EOA,
    dline(),
  ).buildTransaction(tx)

def sign_tx(tx: object, key: str) -> str:
  sig = w3.eth.account.sign_transaction
  return sig(tx, private_key=key)

def send_tx(signed_tx: object) -> str:
  w3.eth.send_raw_transaction(signed_tx.rawTransaction)
  return w3.toHex(w3.keccak(signed_tx.rawTransaction))

def log(tx_hash: str):
  r = w3.eth.wait_for_transaction_receipt(tx_hash)
  s = str({ tx_hash: r})
  with open(LOGS, 'w') as f:
    f.write(s)
    f.close()
    
def buy(tx: object):
  tx_hash = send_tx(sign_tx(tx, KEY))
  print(f'[+] loaded: {tx_hash})')
  log(tx_hash)

def sell(tx: object):
  tx_hash = send_tx(sign_tx(tx, KEY))
  print(f'[-] unload: {tx_hash})')
  log(tx_hash)

# __ SAFETY ___________________________________________________________________

def halt():
  should_buy = 0
  should_sell = 0
  amount_out = getAmountIn(SIZE, res0, res1)
  amount_out += calcSlippage(1, amount_out)
  at_loss = to_exact(router, amount_out, SIZE, WMATIC, USDC)
  sell(at_loss)
  quit()

def safety(price:int):
  if _price < stop_loss:
    halt()

# __ Main _____________________________________________________________________

async def main():
  pair = c_init(PAIR_ADDRESS, fetch_abi('pair.json'))
  router = c_init(ROUTER_ADDRESS, fetch_abi('router.json'))

  should_buy = True
  should_sell = False
  
  cached_stamp = 0
  print('running...')

  while(1):
    res0, res1, stamp = await poll_reserves(pair)
    if stamp > cached_stamp:
      matic_reserve = res0 / 10 ** RES0_DEC
      usdc_reserve = res1 / 10 ** RES1_DEC
      matic_price = usdc_reserve / matic_reserve

      safety(matic_price)

      if matic_price <= demand_zone and should_buy:
        amount_in = getAmountOut(SIZE, res1, res0) 
        amount_in -= calcSlippage(0.5, amount_in)
        at_discount = from_exact(router, SIZE, amount_in, USDC, WMATIC)
        buy(at_discount)

        cached_nonce = w3.eth.get_transaction_count(EOA)
        
        should_buy = False 
        should_sell = True

      elif matic_price >= supply_zone and should_sell:
        amount_out = getAmountIn(SIZE, res0, res1)
        amount_out += calcSlippage(0.5, amount_out)
        at_premium = to_exact(router, amount_out, SIZE, WMATIC, USDC)
        sell(at_premium)

        cached_nonce = w3.eth.get_transaction_count(EOA)

        should_buy = True
        should_sell = False

    cached_stamp = stamp

if __name__ == '__main__':
  asyncio.run(main())
