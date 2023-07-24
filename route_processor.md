# :sushi: Route Processor: route breakdown
---

>> Let's break down the route from this transaction:

- https://polygonscan.com/tx/0xff42abb0a2ffa6e36f72f2eb9cbdf3529ea9a4834415a754b6f857ecc6aa157c

```
0x0301ffff0201cd353f79d9fade311fc3119b841e1f456b54e8580d500b1d8e8ef31e21c99d1db9a6444d3adf1270040d500b1d8e8ef31e21c99d1db9a6444d3adf127000cd353f79d9fade311fc3119b841e1f456b54e85801685e1e383e758b49b3f3413b5c5281c225b2ce1a
```

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
- share: 
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
