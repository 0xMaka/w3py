# @author Maka
# @notice raw post flashbots bundle

from os import getenv 
from dotenv import load_dotenv 
from net import con  

w3 = con('GOERLI')  

load_dotenv()   
EOA = getenv('TRON')   
KEY = getenv('TKEY')    
FLA = getenv('FKEY')


eth_sendBundle = {
  'jsonrpc': "2.0",
  'id': str or int,
  'method': "eth_sendBundle",
  'params': [{
    'txs': [str],               # Array[String], A list of signed transactions to execute in an atomic bundle       
    'blockNumber': str,         # String, a hex encoded block number for which this bundle is valid on       
    'minTimestamp': int,        # (Optional) Number, the minimum timestamp for which this bundle is valid, in seconds since the unix epoch       
    'maxTimestamp': int,        # (Optional) Number, the maximum timestamp for which this bundle is valid, in seconds since the unix epoch       
    'revertingTxHashes': [str], # (Optional) Array[String], A list of tx hashes that are allowed to revert       
    'replacementUuid': str,     # (Optional) String, UUID that can be used to cancel/replace this bundle 
  }]
}

eth_callBundle = {   
  "jsonrpc": "2.0",   
  "id": 1,
  "method": "eth_callBundle",   
  "params": [{       
    "txs": [str,str],       
    "blockNumber": str,
    "stateBlockNumber": str, 
    "timestamp": int  
  }] 
}


def sign_tx(tx, key):   
  return w3.eth.account.sign_transaction(tx, private_key=key)    

from eth_account import messages, Account
def sign_flash(_tx_body: str) -> str:
  message = messages.encode_defunct(text=w3.keccak(text=_tx_body).hex()) 
  signature = f'{Account.from_key(FLA).address}:{w3.eth.account.sign_message(message, FLA).signature.hex()}'
  return signature

from requests import post
def send_flash(_request: dict) -> str:
  request = str(_request).replace("'",'"')
  headers = { 'Content-Type': 'application/json', 'X-Flashbots-Signature': sign_flash(request) }
  return post('https://relay-goerli.flashbots.net', data=request, headers=headers).content


WASTE_GAS = '0x8e63F02d5fB3bCCD2939e0ba6Fe3Bf2635718F49'
SIG = '0x1e0bd6fa'

tx1 = { 'from': EOA, 'to': EOA, 'value': 0, 'chainId': 5, 'gas': 25000, 'maxFeePerGas': w3.to_wei(60, 'gwei'), 'maxPriorityFeePerGas': w3.to_wei(20, 'gwei'), 'data': '0x', 'nonce': w3.eth.get_transaction_count(EOA) }
tx2 = { 'data': SIG, 'to': WASTE_GAS, 'from': EOA,'value': 0,'chainId': 5,'gas': 50000,'maxFeePerGas': w3.to_wei(60, 'gwei'), 'maxPriorityFeePerGas': w3.to_wei(20, 'gwei'),'nonce': w3.eth.get_transaction_count(EOA) + 1}

signed_tx1 = sign_tx(tx1, KEY).rawTransaction.hex()
signed_tx2 = sign_tx(tx2, KEY).rawTransaction.hex()


TARGET_BLOCK = w3.eth.block_number

sim = eth_callBundle; sim.update({'params': [{'txs': [signed_tx1, signed_tx2], 'blockNumber': hex(w3.eth.block_number), 'stateBlockNumber': 'latest'}]})
print(send_flash(sim))

from time import time
bundle = eth_sendBundle
_id = 0
for block_num in range(TARGET_BLOCK, TARGET_BLOCK + 5):
  bundle.update({"id": _id, 'params': [{"txs": [signed_tx1, signed_tx2], "blockNumber": hex(block_num), "minTimestamp": 0, "maxTimestamp": round(time() + 420)}]})
  print(send_flash(bundle))
  _id += 1
