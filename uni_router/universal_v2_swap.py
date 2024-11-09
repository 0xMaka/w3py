#------------------------------------------------------------------------------------------------------------------------------------------#
# UNISWAP UNIVERSAL ROUTER V2 SWAP WITH ONCHAIN PERMIT2 APPROVAL
#------------------------------------------------------------------------------------------------------------------------------------------#

#------------------------------------------------------------------------------------------------------------------------------------------#
# --- FOREWORD ---
#------------------------------------------------------------------------------------------------------------------------------------------#
# This is a variant of the swap from token example targetting a Uniswap v2 pool (as opposed to v3). 
# It was a requested variant, if have similar requests feel free to reach out.

from web3 import Web3; w3 = Web3(Web3.HTTPProvider('https://polygon-rpc.com'))
from os import getenv
from dotenv import load_dotenv
load_dotenv()
eoa = w3.eth.account.from_key(getenv('TKEY'))

#------------------------------------------------------------------------------------------------------------------------------------------#

PERMIT_ADDRESS  = '0x000000000022D473030F116dDEE9F6B43aC78BA3'
TOKEN_ADDRESS   = '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174'
WETH_ADDRESS    = '0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619'
ROUTER_ADDRESS  = '0xec7BE89e9d109e7e3Fec59c222CF297125FEFda2'

# replace with abi in `universal_swap_from_token.py`
ROUTER_ABI = ''
PERMIT_ABI = ''
ERC20_ABI  = ''

router = w3.eth.contract(address=ROUTER_ADDRESS, abi=ROUTER_ABI)
permit = w3.eth.contract(address=PERMIT_ADDRESS, abi=PERMIT_ABI)
token  = w3.eth.contract(address=TOKEN_ADDRESS,  abi=ERC20_ABI )

tx = {
        'from': eoa.address,
        'value': 0,
        'chainId': w3.eth.chain_id,
        'gas': 250000,
        'maxFeePerGas': w3.eth.gas_price,
        'maxPriorityFeePerGas': w3.eth.max_priority_fee * 2,
        'nonce': w3.eth.get_transaction_count(eoa.address)
}

# we will swap on v2 then unwrap wrap the native token

commands = '0x080c'

from eth_abi import encode
from eth_abi.packed import encode_packed
# some sane inputs (sane doesn't mean safe in this case, always use a good slippage value unless protected some other way)
to = router.address  # router here, eoa address in unwrap
amount = 1 * 10 ** 4
slippage = 0
FEE = 10000
path = [TOKEN_ADDRESS, WETH_ADDRESS]
from_eoa = True
unwrap_calldata = encode(['address', 'uint256'], [eoa.address, slippage])
v2_calldata = encode(['address', 'uint256', 'uint256', 'address[]', 'bool'], [to, amount, slippage, path, from_eoa])
deadline = 2*10**10

approve_permit = token.functions.approve(PERMIT_ADDRESS, amount)
approve_router = permit.functions.approve(TOKEN_ADDRESS, ROUTER_ADDRESS, amount, deadline)

#------------------------------------------------------------------------------------------------------------------------------------------#

swap = router.functions.execute(commands, [v2_calldata,unwrap_calldata], deadline).build_transaction(tx)

def sign_tx(tx, key):
  sig = w3.eth.account.sign_transaction
  signed_tx = sig(tx, private_key=key)
  return signed_tx

def send_tx(signed_tx):
  w3.eth.send_raw_transaction(signed_tx.raw_transaction)
  tx_hash = w3.to_hex(w3.keccak(signed_tx.raw_transaction))
  return tx_hash

def main():

  approve1 = approve_permit.build_transaction(tx)
  print ('[-] Approving permit... ')
  tx_hash = send_tx(sign_tx(approve1, eoa.key))
  receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
  print (f'[+] Approved PERMIT2 at TOKEN contract: {tx_hash}\n[>] {receipt}')

  tx.update({'nonce': w3.eth.get_transaction_count(eoa.address)})

  # See signing section of this repo for how to bundle a signature  with the swap
  approve2 = approve_router.build_transaction(tx)
  print ('[-] Approving router... ')
  tx_hash = send_tx(sign_tx(approve2, eoa.key))
  receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
  print (f'[+] Approved ROUTER at PERMIT contract: {tx_hash}\n[>] {receipt}')

  tx.update({'nonce': w3.eth.get_transaction_count(eoa.address)})

  swap = router.functions.execute(commands, [v2_calldata,unwrap_calldata], deadline).build_transaction(tx)
  print(swap)
  print('[-] Simulating swap...')
  w3.eth.call(swap)
  print('[-] Attempting swap...')
  tx_hash = send_tx(sign_tx(swap, eoa.key))
  receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
  print (f'[>] Hash of swap: {tx_hash}\n[>] {receipt}')

if __name__ == '__main__':
  main()

#------------------------------------------------------------------------------------------------------------------------------------------#
