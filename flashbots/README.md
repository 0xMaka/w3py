> :bulb: NOTICE: More recent web3.py versions won't automatically prefix hashes in the signature function, an example of the fix can be found below.

Previously:
```py
message = messages.encode_defunct(text=w3.keccak(text=_tx_body).hex()) 
signature = f'{Account.from_key(FLA).address}:{Account.sign_message(message, FLA).signature.hex()}'
```
Currently:
```py
message = messages.encode_defunct(text='0x' + w3.keccak(text=_tx_body).hex()) 
signature = f'{Account.from_key(FLA).address}:0x{Account.sign_message(message, FLA).signature.hex(
)}'
```
---

# flashbots 🤖
Examples raw posting json rpc calls to flashbots endpoints, useful when features are added to protocol but not yet supprted by the python package.

- More information, along with which fields are optional can be found in the flashbots documentation: 
> https://docs.flashbots.net/flashbots-auction/searchers/advanced/rpc-endpoint

## Calls as python dictionaries:

### eth_sendPrivateTransaction 
- is used to send a single transaction to Flashbots. Flashbots will attempt to build a block including the transaction for the next 25 blocks.
```python
eth_sendPrivateTransaction = {
    'jsonrpc': '2.0',   
    'id': str or int,   
    'method': 'eth_sendPrivateTransaction',
    'params': [{
    'tx': [str],
    'maxBlockNumber': str,     
    'preferences': {       
    'fast': bool,       
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
```

### eth_sendBundle
- can be used to send bundles of two or more transactions to the Flashbots builder.

```python
eth_sendBundle = {
  'jsonrpc': '2.0',
  'id': str or int,
  'method': 'eth_sendBundle',
  'params': [{
    'txs': [str],               # Array[String], A list of signed transactions to execute in an atomic bundle       
    'blockNumber': str,         # String, a hex encoded block number for which this bundle is valid on       
    'minTimestamp': int,        # (Optional) Number, the minimum timestamp for which this bundle is valid, in seconds since the unix epoch       
    'maxTimestamp': int,        # (Optional) Number, the maximum timestamp for which this bundle is valid, in seconds since the unix epoch       
    'revertingTxHashes': [str], # (Optional) Array[String], A list of tx hashes that are allowed to revert       
    'replacementUuid': str,     # (Optional) String, UUID that can be used to cancel/replace this bundle 
  }]
}
```

### eth_callBundle 
- can be used to simulate a bundle against a specific block number, including simulating a bundle at the top of the next block.
```python
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
```

### mev_sendBundle
-  uses a new bundle format to send bundles to MEV-Share.
```python
MevSendBundleParams = {}
mev_sendBundle = {
  'jsonrpc': '2.0',
  'id': str or int,
  'method': 'mev_sendBundle',
  'params': [{ # /* MevSendBundleParams */
  'version': '0' or 'beta-1.0',
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
        'calldata',
        'contract_address',
        'logs',
        'function_selector',
        'hash'
        ],
      'builders': [ str ],
    },
  }]
}   
```
