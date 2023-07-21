# @author Maka
# @notice raw post flashbots private transaction

from os import getenv 
from dotenv import load_dotenv 
from net import con  

w3 = con('GOERLI')  

load_dotenv()   
EOA = getenv('TRON')   
KEY = getenv('TKEY')    
FLA = getenv('FKEY')

def sign_tx(_tx, _key) -> str: 
  return w3.eth.account.sign_transaction(_tx, private_key=_key)

from eth_account import messages, Account
def sign_flash(_tx_body: str) -> str:
  message = messages.encode_defunct(text=w3.keccak(text=_tx_body).hex()) 
  signature = f'{Account.from_key(FLA).address}:{w3.eth.account.sign_message(message, FLA).signature.hex()}'
  return signature

from requests import post
from json import dumps
def send_flash(_request: dict) -> bytes:
  request = dumps(_request)
  headers = { 'Content-Type': 'application/json', 'X-Flashbots-Signature': sign_flash(request) }
  return post('https://relay-goerli.flashbots.net', data=request, headers=headers).content

eth_sendPrivateTransaction = {
    'jsonrpc': '2.0',   
    'id': str or int,   
    'method': 'eth_sendPrivateTransaction',
    'params': [{
    'tx': [str],
    'maxBlockNumber': str,     
    'preferences': {       
    'fast': 'false',       
    'privacy': {            
      'hints': [             
        'contract_address',             
        'function_selector',             
        'calldata',             
        'logs',             
        'hash'         
      ],         
      'builders': [      
        'default',           
        'flashbots'         
      ],       
      }     
    }
  }]
}

TARGET_BLOCK = w3.eth.block_number

WASTE_GAS = '0x8e63F02d5fB3bCCD2939e0ba6Fe3Bf2635718F49'
SIG = '0x1e0bd6fa'
tx = { 'data': SIG, 'to': WASTE_GAS, 'from': EOA,'value':0,'chainId': 5,'gas': 50000,'maxFeePerGas': w3.to_wei('60', 'gwei'), 'maxPriorityFeePerGas': w3.to_wei('20', 'gwei'),'nonce': w3.eth.get_transaction_count(EOA)}
signed_private = sign_tx(tx, KEY).rawTransaction.hex()

private = eth_sendPrivateTransaction
private.update({
  'id': 0,
  'params': [{
    'tx': signed_private, 
    'maxBlockNumber': hex(TARGET_BLOCK + 10),
    'preferences': {       
      'fast': False,       
      'privacy': {            
        'hints': [             
          'contract_address',             
          'function_selector',             
          'calldata',             
          'logs',             
          'hash'         
        ],         
        'builders': [      
          'default',           
          'flashbots'         
        ],       
      }
    }
  }]
})

print(send_flash(private))
 
