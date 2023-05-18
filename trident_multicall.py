from os import getenv
from dotenv import load_dotenv
from net import con
from web3 import Web3
from hexbytes import HexBytes

w3 = con()

def return_account():
  load_dotenv()
  account = {
    'addr': getenv('tron'),
    'key': getenv('key')
  }
  return account

def sign_tx(tx, key):
  sig = w3.eth.account.sign_transaction
  signed_tx = sig(tx, private_key=key)

  return signed_tx

def send_tx(signed_tx):
  w3.eth.send_raw_transaction(signed_tx.rawTransaction)
  tx_hash = w3.toHex(w3.keccak(signed_tx.rawTransaction))

  return tx_hash


def main():

  account = return_account()
  nonce = w3.eth.get_transaction_count(account['addr'])

  usdt = '0xc2132D05D31c914a87C6611C10748AEb04B58e8F'
  wmatic = '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270'
  amountIn = 10000
  amountOutMin = 0

  trident_address = '0xc5017BE80b4446988e8686168396289a9A62668E'
  pool0 = '0xDAE0a6835Fb1c5c09C325F418Be081A9130D818c' # usdt/wmatic

  # pad data
  data0 = ''
  for i in [usdt[2:], trident_address[2:], 1]:
    data0 += '{:0>64}'.format(i) # pad left to 64 bits
  data0 = f'0x{data0}'

  from call_trident import init # grabbing trident instance for encoding
  trident = init()
  swap = trident.encodeABI(fn_name='exactInputSingle', args=[(amountIn, amountOutMin, pool0, usdt, data0)])
  unwrap = trident.encodeABI(fn_name='unwrapWETH', args=[0, account['addr']])
  multicall = trident.encodeABI(fn_name='multicall', args=[[swap,unwrap]])

  tx = {
        'from': account['addr'],
        'to': trident_address,
        'value':0,
        'chainId': 137,
        'gas': 250000,
        'maxFeePerGas': w3.toWei('500', 'gwei'),
        'maxPriorityFeePerGas': w3.toWei('400', 'gwei'),
        'nonce': nonce,
        'data': multicall
        }

  sent = send_tx(sign_tx(tx, account['key']))
  print (f'sent: {sent}')

if __name__ == '__main__':
  main()
