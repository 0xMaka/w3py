We can look at the `commands` contract, to get the list of steps we want to take, then encode the calldata for each of those steps.

In this example we wrap the native coin and then perform a swap on v3.

`commands = '0x0b00'`
```
0b : #    uint256 constant WRAP_ETH = 0x0b; 
00 : #    uint256 constant V3_SWAP_EXACT_IN = 0x00;
```

We can look at the `dispatcher` contract to see what is being decoded on those calls:

```
if (command == Commands.WRAP_ETH) {
 // equivalent: abi.decode(inputs, (address, uint256))
 address recipient;
 uint256 amountMin;
```
For wrapping eth we can see it takes a destination address and amount.
The amount will be the `msg.value` we send with the transaction, the address should be the router as we want to perform a swap after.

For the swap we need:

```
#        address recipient,
#        uint256 amountIn,
#        uint256 amountOutMinimum,
#        bytes calldata path,
#        bool payer
```
A `path` unlike the other values needs "packed encoding", this is the values concatenated without the zero padding.

```python
# (address tokenIn, uint24 fee, address tokenOut)
path = encode_packed(['address','uint24','address'], [WMATIC_ADDRESS, FEE, USDC_ADDRESS])
```
Can think about `payer` as *if from eoa* (your wallet) or the router:
```
False == the router
True  == msg.sender
```

The encoding of the resulting calldata looks like this:
```python
wrap_calldata = encode(['address', 'uint256'], [router.address, amount])
v3_calldata = encode(['address', 'uint256', 'uint256', 'bytes', 'bool'], [to, amount, slippage, path, from_eoa])
```
Finally, we can either encode (not packed) the args together, concatonate with the function sig and use as the calldata in a 
 raw transaction, or simply pass to the `execute` function of a contract instance:
```
swap = router.functions.execute(commands, [wrap_calldata, v3_calldata], deadline).build_transaction(tx)
```

Complete example:
```python
from net import con; w3 = con('POLYGON') # i.e from web3 import Web3; w3 = Web3(Provider(Endpoint))
from os import getenv
from dotenv import load_dotenv
load_dotenv()
KEY = getenv('your_key')
EOA = getenv('your_address')
#----------------------

#---
USDC_ADDRESS = '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174'
WMATIC_ADDRESS = '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270'
WETH_ADDRESS= '0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619'
WMATIC_USDC_ADDRESS = '0xcd353F79d9FADe311fC3119B841e1f456b54e858'
USDC_WETH_ADDRESS = '0x34965ba0ac2451A34a0471F04CCa3F990b8dea27'
ROUTER_ADDRESS = '0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD'

ROUTER_ABI = '''
[{"inputs":[{"components":[{"internalType":"address","name":"permit2","type":"address"},{"internalType":"address","name":"weth9","type":"address"},{"internalType":"address","name":"seaportV1_5","type":"address"},{"internalType":"address","name":"seaportV1_4","type":"address"},{"internalType":"address","name":"openseaConduit","type":"address"},{"internalType":"address","name":"nftxZap","type":"address"},{"internalType":"address","name":"x2y2","type":"address"},{"internalType":"address","name":"foundation","type":"address"},{"internalType":"address","name":"sudoswap","type":"address"},{"internalType":"address","name":"elementMarket","type":"address"},{"internalType":"address","name":"nft20Zap","type":"address"},{"internalType":"address","name":"cryptopunks","type":"address"},{"internalType":"address","name":"looksRareV2","type":"address"},{"internalType":"address","name":"routerRewardsDistributor","type":"address"},{"internalType":"address","name":"looksRareRewardsDistributor","type":"address"},{"internalType":"address","name":"looksRareToken","type":"address"},{"internalType":"address","name":"v2Factory","type":"address"},{"internalType":"address","name":"v3Factory","type":"address"},{"internalType":"bytes32","name":"pairInitCodeHash","type":"bytes32"},{"internalType":"bytes32","name":"poolInitCodeHash","type":"bytes32"}],"internalType":"struct RouterParameters","name":"params","type":"tuple"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"BalanceTooLow","type":"error"},{"inputs":[],"name":"BuyPunkFailed","type":"error"},{"inputs":[],"name":"ContractLocked","type":"error"},{"inputs":[],"name":"ETHNotAccepted","type":"error"},{"inputs":[{"internalType":"uint256","name":"commandIndex","type":"uint256"},{"internalType":"bytes","name":"message","type":"bytes"}],"name":"ExecutionFailed","type":"error"},{"inputs":[],"name":"FromAddressIsNotOwner","type":"error"},{"inputs":[],"name":"InsufficientETH","type":"error"},{"inputs":[],"name":"InsufficientToken","type":"error"},{"inputs":[],"name":"InvalidBips","type":"error"},{"inputs":[{"internalType":"uint256","name":"commandType","type":"uint256"}],"name":"InvalidCommandType","type":"error"},{"inputs":[],"name":"InvalidOwnerERC1155","type":"error"},{"inputs":[],"name":"InvalidOwnerERC721","type":"error"},{"inputs":[],"name":"InvalidPath","type":"error"},{"inputs":[],"name":"InvalidReserves","type":"error"},{"inputs":[],"name":"InvalidSpender","type":"error"},{"inputs":[],"name":"LengthMismatch","type":"error"},{"inputs":[],"name":"SliceOutOfBounds","type":"error"},{"inputs":[],"name":"TransactionDeadlinePassed","type":"error"},{"inputs":[],"name":"UnableToClaim","type":"error"},{"inputs":[],"name":"UnsafeCast","type":"error"},{"inputs":[],"name":"V2InvalidPath","type":"error"},{"inputs":[],"name":"V2TooLittleReceived","type":"error"},{"inputs":[],"name":"V2TooMuchRequested","type":"error"},{"inputs":[],"name":"V3InvalidAmountOut","type":"error"},{"inputs":[],"name":"V3InvalidCaller","type":"error"},{"inputs":[],"name":"V3InvalidSwap","type":"error"},{"inputs":[],"name":"V3TooLittleReceived","type":"error"},{"inputs":[],"name":"V3TooMuchRequested","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"RewardsSent","type":"event"},{"inputs":[{"internalType":"bytes","name":"looksRareClaim","type":"bytes"}],"name":"collectRewards","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes","name":"commands","type":"bytes"},{"internalType":"bytes[]","name":"inputs","type":"bytes[]"}],"name":"execute","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"bytes","name":"commands","type":"bytes"},{"internalType":"bytes[]","name":"inputs","type":"bytes[]"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"execute","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256[]","name":"","type":"uint256[]"},{"internalType":"uint256[]","name":"","type":"uint256[]"},{"internalType":"bytes","name":"","type":"bytes"}],"name":"onERC1155BatchReceived","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"bytes","name":"","type":"bytes"}],"name":"onERC1155Received","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"bytes","name":"","type":"bytes"}],"name":"onERC721Received","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"int256","name":"amount0Delta","type":"int256"},{"internalType":"int256","name":"amount1Delta","type":"int256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"uniswapV3SwapCallback","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]
'''

router = w3.eth.contract(address=ROUTER_ADDRESS, abi=ROUTER_ABI)

#  https://github.com/Uniswap/universal-router/blob/main/contracts/libraries/Commands.sol
#
#    // Command Types where value<0x08, executed in the first nested-if block
#    uint256 constant V3_SWAP_EXACT_IN = 0x00;
#    uint256 constant V3_SWAP_EXACT_OUT = 0x01;
#    uint256 constant PERMIT2_TRANSFER_FROM = 0x02;
#    uint256 constant PERMIT2_PERMIT_BATCH = 0x03;
#    uint256 constant SWEEP = 0x04;
#    uint256 constant TRANSFER = 0x05;
#    uint256 constant PAY_PORTION = 0x06;
#    // COMMAND_PLACEHOLDER = 0x07;
#
#....
#    // Command Types where 0x08<=value<=0x0f, executed in the second nested-if block
#    uint256 constant V2_SWAP_EXACT_IN = 0x08;
#    uint256 constant V2_SWAP_EXACT_OUT = 0x09;
#    uint256 constant PERMIT2_PERMIT = 0x0a;
#    uint256 constant WRAP_ETH = 0x0b;
#    uint256 constant UNWRAP_WETH = 0x0c;
#
# ----

# we will wrap the native coin, then swap on v3

commands = '0x0b00'

# https://github.com/Uniswap/universal-router/blob/main/contracts/base/Dispatcher.sol
#
#                    if (command == Commands.V3_SWAP_EXACT_IN) {
#                        // equivalent: abi.decode(inputs, (address, uint256, uint256, bytes, bool))
#                        address recipient;
#                        uint256 amountIn;
#                        uint256 amountOutMin;
#                        bool payerIsUser
#....
#
#
# https://github.com/Uniswap/universal-router/blob/228f2d151a5fc99836d72ae00f81db92cdb44bd3/contracts/modules/uniswap/v3/V3SwapRouter.sol
#
#    /// @notice Performs a Uniswap v3 exact input swap
#    /// @param recipient The recipient of the output tokens
#    /// @param amountIn The amount of input tokens for the trade
#    /// @param amountOutMinimum The minimum desired amount of output tokens
#    /// @param path The path of the trade as a bytes string
#    /// @param payer The address that will be paying the input
#    function v3SwapExactInput(
#        address recipient,
#        uint256 amountIn,
#        uint256 amountOutMinimum,
#        bytes calldata path,
#        address payer

from eth_abi import encode
from eth_abi.packed import encode_packed
# some sane inputs (sane doesn't mean safe in this case, always use a good slippage value unless protected some other way)
to = EOA
amount = 1 * 10 ** 17
slippage = 0
FEE = 500
# (address tokenIn, uint24 fee, address tokenOut)
path = encode_packed(['address','uint24','address'], [WMATIC_ADDRESS, FEE, USDC_ADDRESS])
from_eoa = False # the router or user? router after wrapping

wrap_calldata = encode(['address', 'uint256'], [router.address, amount])
v3_calldata = encode(['address', 'uint256', 'uint256', 'bytes', 'bool'], [to, amount, slippage, path, from_eoa])

deadline = 2*10**10

print(commands)
print(wrap_calldata.hex())
print(v3_calldata.hex())
print(deadline)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------

tx = {
        'from': EOA,
        'value': amount,
        'chainId': 137,
        'gas': 250000,
        'maxFeePerGas': w3.eth.gas_price * 2,
        'maxPriorityFeePerGas': w3.eth.max_priority_fee * 2,
        'nonce': w3.eth.get_transaction_count(EOA)
}

def sign_tx(tx, key):
  sig = w3.eth.account.sign_transaction
  signed_tx = sig(tx, private_key=key)
  return signed_tx

def send_tx(signed_tx):
  w3.eth.send_raw_transaction(signed_tx.rawTransaction)
  tx_hash = w3.to_hex(w3.keccak(signed_tx.rawTransaction))
  return tx_hash

def main():
  swap = router.functions.execute(commands, [wrap_calldata, v3_calldata], deadline).build_transaction(tx)
  print(swap)
  print('[-] Simulating swap...')
  w3.eth.call(swap)
  print('[-] Attempting swap...')
  tx_hash = send_tx(sign_tx(swap, KEY))
  receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
  print (f'[>] Hash of swap: {tx_hash}\n[>] {receipt}')

if __name__ == '__main__':
  main()
```
