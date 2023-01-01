from os import getenv
from dotenv import load_dotenv
from net import con

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
  
  pool0 = '0xDAE0a6835Fb1c5c09C325F418Be081A9130D818c' # usdt/wmatic
  pool1 = '0x42d9B05962ab52b17f5F1854DA7d3eC89ad4081A' # wmatic/sushi 
  
  # pad data
  data0 = ''
  for i in [usdt[2:], pool1[2:], 0]:
    data0 += '{:0>64}'.format(i) # pad left to 64 bits
  data0 = f'0x{data0}'
  
  data1 = ''
  for i in [wmatic[2:], account['addr'][2:], 0]:
    data1 += '{:0>64}'.format(i) # pad left to 64 bits
  data1 = f'0x{data1}'

  from call_trident import init # grabbing trident instance for encoding
  trident = init()
  encoded = trident.encodeABI(fn_name='exactInput', args=[(usdt, amountIn, amountOutMin, [[pool0, data0], [pool1, data1]])])

  tx = {
        'from': account['addr'],
        'value':0,
        'chainId': 137,
        'gas': 250000,
        'maxFeePerGas': w3.toWei('50', 'gwei'),
        'maxPriorityFeePerGas': w3.toWei('40', 'gwei'),
        'nonce': nonce,
        'data': encoded
        }
  
  trident = '0xc5017BE80b4446988e8686168396289a9A62668E'
  tx.update({'to': trident})
  
  sent = send_tx(sign_tx(tx, account['key']))
  print (f'sent: {sent}') 

if __name__ == '__main__':
  main()
