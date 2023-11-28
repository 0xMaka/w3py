# deprecated signing examples 

from web3 import Web3, HTTPProvider
# generally don't share your endpoints
w3 = Web3(HTTPProvider('https://eth-goerli.g.alchemy.com/v2/...'))
# NEVER SHARE PRIVATE KEYS
example_key = b"\xb2\\}\xb3\x1f\xee\xd9\x12''\xbf\t9\xdcv\x9a\x96VK-\xe4\xc4rm\x03[6\xec\xf1\xe5\xb3d".hex()
keys_address = '0x5ce9454909639d2d17a3f753ce7d93fa0b9ab12e'

print(f'''[x] Deprecated signing example:
[>] PRIVATE KEY: {example_key} [NOTE: THIS KEY IS FROM DOCUMENTATION, FOR EXAMPLE ONLY. NEVER SHARE YOUR PRIVATE KEYS!!]
[>] EOA (keys address): {keys_address}
''')

# From the web3.py docs..
# There is no single message format that is broadly adopted with community consensus.
# Keep an eye on several options, like EIP-683, EIP-712, and EIP-719. 
# Consider the w3.eth.sign() approach be deprecated. 

# deprecated method
from eth_account.messages import encode_defunct
msg = 'if it requires trust it\'s sus'
encoded_msg = encode_defunct(text=msg)

signed_message = w3.eth.account.sign_message(encoded_msg, private_key=example_key)
print(f'[+] signed_message: \n{signed_message}\n')
print(f'[>] v: {signed_message.v}')
print(f'[>] r: {signed_message.r}')
print(f'[>] s: {signed_message.s}')
print(f'[>] signature: {signed_message.signature.hex()}\n')

# verifying the sender in python, with deprecated method.
result = w3.eth.account.recover_message(encoded_msg, signature=signed_message.signature)
print(f'[+] Result of recovery: {result}')
print(f'[+] Matches address\n') if result.lower() == keys_address.lower() else print('[!] Mismatch\n')

# simple vyper contract for testing
verify_sig_source = '''
# @version 0.3.7
# @title verify_sig.vy

@external 
@view
def get_hash(_str: String[80]) -> bytes32:     
  return keccak256(_str)  

@external
@view 
def get_signed_hash(_hash: bytes32) -> bytes32:     
# The initial 0x19 byte is intended to ensure that the signed_data is not valid RLP.
# 32 is the length of appended data in bytes.
  return keccak256(         
    concat(             
      b'\\x19Ethereum Signed Message:\\n32', # double backslash not needed in a native vy file            
      _hash         
    )     
  )   

@external 
@view 
def verify(_signed_hash: bytes32, _sig: Bytes[65]) -> address:     
  r: uint256 = convert(slice(_sig, 0, 32), uint256)     
  s: uint256 = convert(slice(_sig, 32, 32), uint256)     
  v: uint256 = convert(slice(_sig, 64, 1), uint256)     
  return ecrecover(_signed_hash, v, r, s)

'''
# compiling the contract
from vyper import compiler
out = compiler.compile_code(verify_sig_source,['abi', 'bytecode'])

# is already deployed on goerli for easy testing so can create an instance using the address, and abi
## Verify Sig Contract
vsc = w3.eth.contract(address='0x0A4089a64A88D0317ac2E683696Fa9C69b2C7092', abi=out['abi']).functions

msg_from_contract = vsc.get_hash('if it requires trust it\'s sus').call()
print(f'[<] msg_from_contract: {msg_from_contract.hex()}')

signed_msg_from_contract = vsc.get_signed_hash(msg_from_contract).call()
print(f'[<] signed_msg_from_contract: {signed_msg_from_contract.hex()}\n')

# using the depreciated method to sign for a contract
from eth_account.messages import _hash_eip191_message

#encode
msg_for_contract = encode_defunct(hexstr=msg_from_contract.hex()) # same as signed_message_from_contract
print(f'[>] msg_for_contract: { msg_for_contract}\n')

# hash explicitely
signed_msg_for_contract = _hash_eip191_message(msg_for_contract)
print(f'[>] signed_msg_for_contract: { signed_msg_for_contract.hex()}')

print('[+] Matches signed_msg_from_contract\n') if signed_msg_for_contract.hex() == signed_msg_from_contract.hex() else print('[!] Mismatch\n')

signed_for_contract = w3.eth.account.sign_message(msg_for_contract, private_key=example_key)
print(f'[+] signed_for_contract: {signed_for_contract}\n')

print(f'[>] signed_for_contract.messageHash: {signed_for_contract.messageHash.hex()}')
print(f'[>] signed_for_contract.signature: {signed_for_contract.signature.hex()}\n')

result_from_contract = vsc.verify(signed_for_contract.messageHash, signed_for_contract.signature).call()
print(f'[+] result_from_contract: {result_from_contract}')
print(f'[+] Matches address\n') if result_from_contract.lower() == keys_address.lower() else print('[!] Mismatch\n')
