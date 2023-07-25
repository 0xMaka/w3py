# Route Processor: route breakdown (with working example)
---
To build a route you'll want to know what you want to do, then look for those stages in the contract.
There are command bytes and pool bytes which are uint8, there is a share parameter which is uint16 and there are pool and token addresses.
You will need to either abi packed encode, or concatenate their unpadded hex values.

ex.
```python
from eth_abi.packed import encode_packed
route = encode_packed(['uint8', 'address', 'uint8', 'uint16', 'uint8', 'address', 'uint8', 'address'], [source, token_in, num, share, pool_type, pair, direction, to])
```

Let's break down the route from this transaction:
- https://polygonscan.com/tx/0xff42abb0a2ffa6e36f72f2eb9cbdf3529ea9a4834415a754b6f857ecc6aa157c

Route code:
```
0x0301ffff0201cd353f79d9fade311fc3119b841e1f456b54e8580d500b1d8e8ef31e21c99d1db9a6444d3adf1270040d500b1d8e8ef31e21c99d1db9a6444d3adf127000cd353f79d9fade311fc3119b841e1f456b54e85801685e1e383e758b49b3f3413b5c5281c225b2ce1a
```
Broken up:
>03 01 ffff 02 01 
>cd353f79d9fade311fc3119b841e1f456b54e858 
>0d500b1d8e8ef31e21c99d1db9a6444d3adf1270 
>04 
>0d500b1d8e8ef31e21c99d1db9a6444d3adf1270 
>00 
>cd353f79d9fade311fc3119b841e1f456b54e858 
>01 
>685e1e383e758b49b3f3413b5c5281c225b2ce1a

### command 03
(commandCode == 3) processNative(stream);
```solidity
  /// @notice Processes native coin: call swap for all pools that swap from native coin
  /// @param stream Streamed process program
  function processNative(uint256 stream) private {
    uint256 amountTotal = address(this).balance;
    distributeAndSwap(stream, address(this), NATIVE_ADDRESS, amountTotal);
  }
```
- num of routes: 
- - 01
- share from route: 
- - ffff
```solidity
  /// @notice Distributes amountTotal to several pools according to their shares and calls swap for each pool
  /// @param stream Streamed process program
  /// @param from Where to take liquidity for swap
  /// @param tokenIn Input token
  /// @param amountTotal Total amount of tokenIn for swaps 
  function distributeAndSwap(uint256 stream, address from, address tokenIn, uint256 amountTotal) private {
    uint8 num = stream.readUint8();
    unchecked {
      for (uint256 i = 0; i < num; ++i) {
        uint16 share = stream.readUint16();
        uint256 amount = (amountTotal * share) / 65535;
        amountTotal -= amount;
        swap(stream, from, tokenIn, amount);
      }
    }
  }

```
### pool type: 02
(poolType == 2) wrapNative(stream, from, tokenIn, amountIn);

```solidity
  /// @notice Makes swap
  /// @param stream Streamed process program
  /// @param from Where to take liquidity for swap
  /// @param tokenIn Input token
  /// @param amountIn Amount of tokenIn to take for swap
  function swap(uint256 stream, address from, address tokenIn, uint256 amountIn) private {
    uint8 poolType = stream.readUint8();
    if (poolType == 0) swapUniV2(stream, from, tokenIn, amountIn);
    else if (poolType == 1) swapUniV3(stream, from, tokenIn, amountIn);
    else if (poolType == 2) wrapNative(stream, from, tokenIn, amountIn);
    else if (poolType == 3) bentoBridge(stream, from, tokenIn, amountIn);
    else if (poolType == 4) swapTrident(stream, from, tokenIn, amountIn);
    else revert('RouteProcessor: Unknown pool type');
  }
```

- direction and fake: 
- - 01
- to (pair): 
-  - cd353f79d9fade311fc3119b841e1f456b54e858 
- wrap token (matic): 
- - 0d500b1d8e8ef31e21c99d1db9a6444d3adf1270

```solidity
  /// @notice Wraps/unwraps native token
  /// @param stream [direction & fake, recipient, wrapToken?]
  /// @param from Where to take liquidity for swap
  /// @param tokenIn Input token
  /// @param amountIn Amount of tokenIn to take for swap
  function wrapNative(uint256 stream, address from, address tokenIn, uint256 amountIn) private {
    uint8 directionAndFake = stream.readUint8();
    address to = stream.readAddress();

    if (directionAndFake & 1 == 1) {  // wrap native
      address wrapToken = stream.readAddress();
      if (directionAndFake & 2 == 0) IWETH(wrapToken).deposit{value: amountIn}();
      if (to != address(this)) IERC20(wrapToken).safeTransfer(to, amountIn);
    } else { // unwrap native
      if (directionAndFake & 2 == 0) {
        if (from != address(this)) IERC20(tokenIn).safeTransferFrom(from, address(this), amountIn);
        IWETH(tokenIn).withdraw(amountIn);
      }
      payable(to).transfer(address(this).balance);
    }
  }
 ``` 

### command 04
(commandCode == 4) processOnePool(stream);
- token (matic):
- - 0d500b1d8e8ef31e21c99d1db9a6444d3adf1270  
```solidity
  /// @notice Processes ERC20 token for cases when the token has only one output pool
  /// @notice In this case liquidity is already at pool balance. This is an optimization
  /// @notice Call swap for all pools that swap from this token
  /// @param stream Streamed process program
  function processOnePool(uint256 stream) private {
    address token = stream.readAddress();
    swap(stream, address(this), token, 0);
  }
```

### pool type 0
(poolType == 0) swapUniV2(stream, from, tokenIn, amountIn);

- pool: 
- - cd353f79d9fade311fc3119b841e1f456b54e858 
- direction: 
- - 01
- to (destination wallet): 
- - 685e1e383e758b49b3f3413b5c5281c225b2ce1a

```solidity
  /// @notice UniswapV2 pool swap
  /// @param stream [pool, direction, recipient]
  /// @param from Where to take liquidity for swap
  /// @param tokenIn Input token
  /// @param amountIn Amount of tokenIn to take for swap
  function swapUniV2(uint256 stream, address from, address tokenIn, uint256 amountIn) private {
    address pool = stream.readAddress();
    uint8 direction = stream.readUint8();
    address to = stream.readAddress();

    (uint256 r0, uint256 r1, ) = IUniswapV2Pair(pool).getReserves();
    require(r0 > 0 && r1 > 0, 'Wrong pool reserves');
    (uint256 reserveIn, uint256 reserveOut) = direction == 1 ? (r0, r1) : (r1, r0);

    if (amountIn != 0) {
      if (from == address(this)) IERC20(tokenIn).safeTransfer(pool, amountIn);
      else IERC20(tokenIn).safeTransferFrom(from, pool, amountIn);
    } else amountIn = IERC20(tokenIn).balanceOf(pool) - reserveIn;  // tokens already were transferred

    uint256 amountInWithFee = amountIn * 997;
    uint256 amountOut = (amountInWithFee * reserveOut) / (reserveIn * 1000 + amountInWithFee);
    (uint256 amount0Out, uint256 amount1Out) = direction == 1 ? (uint256(0), amountOut) : (amountOut, uint256(0));
    IUniswapV2Pair(pool).swap(amount0Out, amount1Out, to, new bytes(0));
```


A working example:

- This script swaps .5 matic to usdc on Polygon mainnet.

| WARNING          |
|:---------------------------|
| Please note that 0 is used for amountOutMin here, but you should always use the amount out you want minus a percent slippage you are willing to take, if front running is a concern.|

```python
# imports and initialisations (can ignore)
from net import con; w3 = con('POLYGON') # i.e from web3 import Web3; w3 = Web3(Provider(Endpoint))
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

# if (commandCode == 2) processUserERC20(stream, amountIn);
source = 0x02

# function processUserERC20(uint256 stream, uint256 amountTotal) private {
#   address token = stream.readAddress();
token_in = WMATIC_ADDRESS

# uint8 num = stream.readUint8();
# ..uint16 share = stream.readUint16();
num = 0x01 # 1 route
share = 0xffff # full amount

# function swap(uint256 stream, address from, address tokenIn, uint256 amountIn) private {
#   uint8 poolType = stream.readUint8();
#   if (poolType == 0) swapUniV2(stream, from, tokenIn, amountIn);
pool_type = 0x00

 # function swapUniV2(uint256 stream, address from, address tokenIn, uint256 amountIn) private {
 #   address pool = stream.readAddress();
 #   uint8 direction = stream.readUint8();
 #   address to = stream.readAddress();
pair = WMATIC_USDC_ADDRESS
direction = 0x01 # token 1 to 0 or 0 to 1 (check pool or call it and sort them)
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

def sign_tx(tx, key):
  sig = w3.eth.account.sign_transaction
  signed_tx = sig(tx, private_key=key)
  return signed_tx

def send_tx(signed_tx):
  w3.eth.send_raw_transaction(signed_tx.rawTransaction)
  tx_hash = w3.to_hex(w3.keccak(signed_tx.rawTransaction))
  return tx_hash

def main():
  approve = wmatic.functions.approve(ROUTER_ADDRESS, 500000000000000000).build_transaction(tx)
  print ('[-] Approving... ')
  tx_hash = send_tx(sign_tx(approve, KEY))
  receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
  print (f'[+] approved: {tx_hash}\n[>] {receipt}')

  tx.update({'nonce': w3.eth.get_transaction_count(EOA)})
  swap = router.functions.processRoute(
    WMATIC_ADDRESS,
    500000000000000000,
    USDC_ADDRESS,
    0,
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
```
