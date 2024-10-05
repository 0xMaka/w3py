from os import getenv
from dotenv import load_dotenv
from net import con

w3 = con()

def return_account():
  load_dotenv()
  return { 'addr': getenv('tron'), 'key': getenv('key') }

def sign_tx(tx, key):
  sig = w3.eth.account.sign_transaction
  return sig(tx, private_key=key)

def send_tx(signed_tx):
  w3.eth.send_raw_transaction(signed_tx.rawTransaction)
  return w3.toHex(w3.keccak(signed_tx.rawTransaction))

def main():

  account = return_account() 
  nonce = w3.eth.get_transaction_count(account['addr'])
  tx = {
        'from': account['addr'],
        'value':0,
        'chainId': 42,
        'gas': 500000,
        'maxFeePerGas': w3.toWei('50', 'gwei'),
        'maxPriorityFeePerGas': w3.toWei('40', 'gwei'),
        'nonce': nonce
        }
  
  data = ''
  with open('vy/test.bin', 'r') as f:
    data = f.read()
    
  tx.update({'data': data.strip()})
  
  sent = send_tx(sign_tx(tx, account['key']))
  print (f'sent: {sent}') 

if __name__ == '__main__':
  main()
