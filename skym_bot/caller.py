# @title caller.py - skym_bot
# @notice simple skim bot example flow, with py and vy.

#  NOTE: Bot makes no check for profitability, only difference. Bot scans a single pool. 
#        Bot makes no attempt to optimise cycles and would not be competative.
#        To make competative bots consider writing computationally expensive modules in c,
#        or rust, and using python as the glue language.
#        Consider strategies for gas, and pool analysis.
#        Consider running an own node or looking into a service such as block native,
#        so to back run the mem pool as opposed to on chain balance changes.
#
#        1love
#

# @author Maka

# imports
from os import getenv

from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv

import asyncio

# initializations & declerations
load_dotenv()
w3 = Web3(HTTPProvider(getenv('NODE')))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

acc = getenv('ACC')
key = getenv('KEY')

fn_hash = '0xbc25cf77'
fn_call = '{:0>64}'.format(acc[2:])
SKIM = f'{fn_hash}{fn_call}'
RELAY ='0x19FDA656Ffb0C51420832A42ed319a0fEDD6477f' # relay contract address

# helper - fetches abi from file located in 'abi/'
def from_json(file: str) -> str:
  with open(file) as f:
    abi = f.read().strip()
    f.close()
    return abi

SLP_ABI = from_json('abi/slp_abi.json')
ERC20_ABI = from_json('abi/erc20_abi.json')
RELAY_ABI = from_json('abi/relay_abi.json')

# helper - returns a w3 contract object
def conify(add: str, abi: str) -> object:
  return w3.eth.contract(address=add, abi=abi)

eth_usdc = '0x19DA2E185dB2842710FDed575E9da96c66cc4025' # sushi on goerli
slp = conify(eth_usdc, SLP_ABI)
relay = conify(RELAY, RELAY_ABI)

# core functions
def get_reserves(slp: object) -> list:
  reserve0, reserve1, timestamp = slp.functions.getReserves().call()
  del(timestamp)
  return [reserve0, reserve1]

def sort_tokens(slp: object) -> list:
  token0 = slp.functions.token0().call()
  token1 = slp.functions.token1().call()
  return [token0, token1]

def get_balances(slp: object) -> list:
  tokens = []
  for i in sort_tokens(slp):
    tokens.append(conify(i, ERC20_ABI))
  token0_bal = tokens[0].functions.balanceOf(slp.address).call()
  token1_bal = tokens[1].functions.balanceOf(slp.address).call()
  return [token0_bal, token1_bal]

def fetch_amounts(slp: object) -> dict:
  r0, r1 = get_reserves(slp)
  b0, b1 = get_balances(slp)
  return {
    'reserve0': r0,
    'balance0': b0,

    'reserve1': r1,
    'balance1': b1,
  }

# @params [reserve0, balance0, reserve1, balance1]
def sort_gt(vals: list) -> str:
  return 'token0' if vals[1] > vals[0] else 'token1'

def sign_tx(tx, key) -> str:
  sig = w3.eth.account.sign_transaction
  return sig(tx, private_key=key)

def send_tx(signed_tx) -> str:
  w3.eth.send_raw_transaction(signed_tx.rawTransaction)
  return w3.toHex(w3.keccak(signed_tx.rawTransaction))

def confirm_tx(tx_hash) -> (dict, bool):
  try:
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120, poll_latency=0.1)
    return (receipt, 1)
  except: return ({'Status': 'Failed'}, 0)

def get_tx() -> dict:
  return {
        'from': acc,
        'value':0,
        'chainId': 5,
        'gas': 500000,
        'maxFeePerGas': w3.toWei('50', 'gwei'),
        'maxPriorityFeePerGas': w3.toWei('40', 'gwei'),
        'nonce': w3.eth.get_transaction_count(acc)
        }

def pj(d: dict) -> str:
  for key, value in d.items():
    print(f'{key}: {value}')

def go_skim(pool: str, tx: dict) -> str:
  rtx = relay.functions.fn_relay(pool, SKIM).build_transaction(tx)
  return send_tx(sign_tx(rtx, key))

async def main():
  token0, token1 = sort_tokens(slp)
  success = False

  print('--- [+] Incoming data --------------------------------------#')

  while(1): # run forever
    res0, bal0, res1, bal1 = fetch_amounts(slp).values()
    vals = [res0, bal0, res1, bal1]
    diff = [vals[1] - vals[0], vals[3] - vals[2]]
    print(
      f'''\nToken0: {token0} \n  res0: {vals[0]}\n  bal0: {vals[1]}\n  diff: {diff[0]}  
          \nToken1: {token1} \n  res1: {vals[2]}\n  bal1: {vals[3]}\n  diff: {diff[1]}'''
    )

    if diff[0] >= 5*10**14 or diff[1] >= 1*10**6: # if difference gte roughly '$1'
      tx = get_tx()
      #....
      gt = sort_gt(vals)
      address = token0 if gt == 'token0' else token1
      print('\n------------------------------------------------------------#\n')
      print(f'[+] {gt}:\n    {address}\n    Shows diff: {diff[int(gt[-1:])]}') # 0|1

      tx_hash = go_skim(slp.address, tx)
      print(f'[+] Tx launched: {tx_hash}')

      print(f'[+] Awaiting receipt...')
      receipt, success = confirm_tx(tx_hash) 

      if success:
        print(f'[+] Tx receipt: ')
        pj(vars(receipt))
      elif not success:
        tx.update({
          'maxFeePerGas': w3.toWei('60', 'gwei'),
          'maxPriorityFeePerGas': w3.toWei('50', 'gwei')
        })
        tx_hash = go_skim(slp.address, tx)
        print(f'[+] Replacement tx launched: {tx_hash}')
        print(f'[+] Awaiting receipt...')
        print(confirm_tx(tx_hash)) 
      else: 
        print('Some error')
    
    print('\n------------------------------------------------------------#')
    await asyncio.sleep(3)

asyncio.run(main())
