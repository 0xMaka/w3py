# imports and initialisations (can ignore)
from net import con; w3 = con('POLYGON')
# account
from os import getenv
from dotenv import load_dotenv
load_dotenv()
KEY = getenv('TKEY')
EOA = getenv('TRON')
#----------------------


#---
USDC_ADDRESS = '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174'
WMATIC_ADDRESS = '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270'
WMATIC_USDC_ADDRESS = '0xcd353F79d9FADe311fC3119B841e1f456b54e858'

ROUTER_ADDRESS = '0x0a6e511Fe663827b9cA7e2D2542b20B37fC217A6'

ROUTER_ABI = '''[{"inputs":[{"internalType":"address","name":"_bentoBox","type":"address"},{"internalType":"address[]","name":"priviledgedUserList","type":"address[]"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":false,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"address","name":"tokenIn","type":"address"},{"indexed":true,"internalType":"address","name":"tokenOut","type":"address"},{"indexed":false,"internalType":"uint256","name":"amountIn","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amountOut","type":"uint256"}],"name":"Route","type":"event"},{"inputs":[],"name":"bentoBox","outputs":[{"internalType":"contract IBentoBoxMinimal","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"route","type":"bytes"}],"name":"processRoute","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"resume","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"bool","name":"priviledge","type":"bool"}],"name":"setPriviledge","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address payable","name":"transferValueTo","type":"address"},{"internalType":"uint256","name":"amountValueTransfer","type":"uint256"},{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"route","type":"bytes"}],"name":"transferValueAndprocessRoute","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"int256","name":"amount0Delta","type":"int256"},{"internalType":"int256","name":"amount1Delta","type":"int256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"uniswapV3SwapCallback","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'''
ERC20_ABI = ''' [{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"guy","type":"address"},{"name":"wad","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"src","type":"address"},{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"wad","type":"uint256"}],"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"deposit","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"guy","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Withdrawal","type":"event"}] '''

router = w3.eth.contract(address=ROUTER_ADDRESS, abi=ROUTER_ABI)
wmatic = w3.eth.contract(address=WMATIC_ADDRESS, abi=ERC20_ABI)

# ----



# what do I want to do.. use pre wrapped matic from wallet and swap for usdc.. 
# lets work through the contract like shown in the walk through example @ https://github.com/0xMaka/w3py/blob/main/route_processor.md

# if (commandCode == 2) processUserERC20(stream, amountIn);
source = 0x02

#function processMyERC20(uint256 stream) private {
#   address token = stream.readAddress();
token_in = WMATIC_ADDRESS

# uint8 num = stream.readUint8();
# ..uint16 share = stream.readUint16();
num = 0x01
share = 0xffff

# function swap(uint256 stream, address from, address tokenIn, uint256 amountIn) private {
#   uint8 poolType = stream.readUint8();
#   if (poolType == 0) swapUniV2(stream, from, tokenIn, amountIn);

pool_type = 0x00

 # function swapUniV2(uint256 stream, address from, address tokenIn, uint256 amountIn) private {
 #   address pool = stream.readAddress();
 #   uint8 direction = stream.readUint8();
 #   address to = stream.readAddress();
pair = WMATIC_USDC_ADDRESS
direction = 0x01
to = EOA

from eth_abi.packed import encode_packed
route = encode_packed(['uint8', 'address', 'uint8', 'uint16', 'uint8', 'address', 'uint8', 'address'], [source, token_in, num, share, pool_type, pair, direction, to])

PROCESSED_ROUTE = f'0x{route.hex()}'
print(PROCESSED_ROUTE)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------


# driver
tx = {
        'from': EOA,
        'value':0,
        'chainId': 137,
        'gas': 250000,
        'maxFeePerGas': w3.eth.gas_price * 2,
        'maxPriorityFeePerGas': w3.to_wei('40', 'gwei'),
        'nonce': w3.eth.get_transaction_count(EOA)
}

# helpers
def sign_tx(tx, key):
  sig = w3.eth.account.sign_transaction
  signed_tx = sig(tx, private_key=key)
  return signed_tx

def send_tx(signed_tx):
  w3.eth.send_raw_transaction(signed_tx.rawTransaction)
  tx_hash = w3.to_hex(w3.keccak(signed_tx.rawTransaction))
  return tx_hash

def main():
  approve = wmatic.functions.approve(ROUTER_ADDRESS, AMOUNT_IN).build_transaction(tx)
  print ('[-] Approving... ')
  tx_hash = send_tx(sign_tx(approve, KEY))
  receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
  print (f'[+] approved: {tx_hash}\n[>] {receipt}')

  tx.update({'nonce': w3.eth.get_transaction_count(EOA)})
  swap = router.functions.processRoute(
    WMATIC_ADDRESS,
    500000000000000000, # AMOUNT_IN,
    USDC_ADDRESS,
    0, # AMOUNT_OUT_WITH_SLIPPAGE,
    EOA,
    PROCESSED_ROUTE
  ).build_transaction(tx)
  print('[-] Simulating swap...')
  w3.eth.call(swap)
  print('[-] Attempting swap...')
  tx_hash = send_tx(sign_tx(swap, KEY))
  receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
  print (f'[>] Hash of swap: {tx_hash}\n[>] {receipt}')

if __name__ == '__main__':
  main()
 # pass
