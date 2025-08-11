# @author Maka
# @notice raw post flashbots mevshare bundle

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
  message = messages.encode_defunct(text=w3.keccak(text=_tx_body).to_0x_hex()) 
  signature = f'{Account.from_key(FLA).address}:{w3.eth.account.sign_message(message, FLA).signature.to_0x_hex()}'
  return signature

from requests import post
from json import dumps
def send_flash(_request: dict) -> bytes:
  request = dumps(_request)
  headers = { 'Content-Type': 'application/json', 'X-Flashbots-Signature': sign_flash(request) }
  return post('https://relay-goerli.flashbots.net', data=request, headers=headers).content


MevSendBundleParams = {}
mev_sendBundle = {
  'jsonrpc': "2.0",
  'id': str or int,
  'method': "mev_sendBundle",
  'params': [{ # /* MevSendBundleParams */
              'version': "0" or "beta-1.0",
    'inclusion': {
      'block': str,      # // hex-encoded number
      'maxBlock': str,  # // hex-encoded number
    },
    'body': [
      { 'hash': str },
      { 'tx': str, 'canRevert': bool },
      { 'bundle': MevSendBundleParams }
      ],
    'validity': {
      'refund': [{
        'bodyIdx': int,
        'percent': int,
      }],
      'refundConfig': [{
        'address': str,
        'percent': int,
      }],
    },
    'privacy': {
      'hints': [
        "calldata",
        "contract_address",
        "logs",
        "function_selector",
        "hash"
        ],
      'builders': [ str ],
    },
  }]
}

eth_callBundle = {   
  'jsonrpc': '2.0',   
  'id': 1,
  'method': 'eth_callBundle',   
  'params': [{       
    'txs': [str,str],       
    'blockNumber': str,
    'stateBlockNumber': str, 
    'timestamp': int  
  }] 
}

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

FREE = '0x9F4D93A220c23C786243a1406Dc69FCd8f4DAC35'
TOGGLE = '0x47194a85'
TAKE = '0xe0f6be56'

TARGET_BLOCK = w3.eth.block_number

tx1 = { 'data': TOGGLE, 'to': FREE, 'from': EOA,'value': 0,'chainId': 5,'gas': 40000,'maxFeePerGas': w3.to_wei('60', 'gwei'),'maxPriorityFeePerGas': w3.to_wei('20', 'gwei'),'nonce': w3.eth.get_transaction_count(EOA)}
tx2 = { 'data': TAKE, 'to': FREE, 'from': EOA,'value':0,'chainId': 5,'gas': 50000,'maxFeePerGas': w3.to_wei('60', 'gwei'), 'maxPriorityFeePerGas': w3.to_wei('20', 'gwei'),'nonce': w3.eth.get_transaction_count(EOA) + 1}

signed_private = sign_tx(tx1, KEY).rawTransaction.to_0x_hex()
signed_backrun = sign_tx(tx2, KEY).rawTransaction.to_0x_hex()

private = eth_sendPrivateTransaction
private.update({
  'id': 420,
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

bundle = mev_sendBundle 
bundle.update ({
  'method': 'mev_sendBundle',
  'id': 0,
  'params': [{
    'version': 'v0.1',
    'inclusion': {
      'block': hex(TARGET_BLOCK),
      'maxBlock': hex(TARGET_BLOCK + 25)
    },
    'body': [{'tx': signed_private, 'canRevert': False}, {'tx': signed_backrun, 'canRevert': False}],
#    'validity': {'refund': [{ 'bodyIdx': 1, 'percent': 90}]}
  }]
})

# send private tx
print(send_flash(private))

# simulate bundle
sim = eth_callBundle; sim.update({'params': [{'txs': [signed_private, signed_backrun], 'blockNumber': hex(w3.eth.block_number), 'stateBlockNumber': 'latest'}]})
print(send_flash(sim))

# target next few blocks
_id = 0
_target = TARGET_BLOCK
for block_num in range(TARGET_BLOCK, TARGET_BLOCK + 5):
  bundle.update({"id": _id}), 
  bundle['params'][0]['inclusion'] = {'block': hex(_target), 'maxBlock': hex(_target + 5)}
  print(send_flash(bundle))
  _id += 1
  _target += 1


# see if bundle was matched
bundle['method'] =  'mev_simBundle'
_id = 0
_target = TARGET_BLOCK
for block_num in range(TARGET_BLOCK, TARGET_BLOCK + 5):
  bundle.update({"id": _id}), 
  bundle['params'][0]['inclusion'] = {'block': hex(_target), 'maxBlock': hex(_target + 5)}
  response = send_flash(bundle)
  if b'success' in response:
    print(response)
    break
  _id += 1
  _target += 1
 
