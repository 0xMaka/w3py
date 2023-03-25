# Trident help sheet
---
Enough to work out the rest

### Keyword: Native
 - Means from the users wallet here, rather than the gas token.

So exactInputSingle(), swaps on a single pool, from a token already in the EOA's (**Externally Owned** wallet's), Bentobox **Account**.
exactInputSingleNative() swaps on a single pool, but takes the token from the EOA's wallet. Approvals will be needed.

For these single pool swaps the data we pass is the following:

![](https://i.imgur.com/i2ppYFI.png)


token A:

![](https://i.imgur.com/vzOZU4s.png)

amount  of token A to swap:

![](https://i.imgur.com/mPncrkl.png)

minimum amount of token B after the swap:

![](https://i.imgur.com/GTAl556.png)


Though what's the data, required by the pool for the swap?
Let's check ITridentRouter:

![](https://i.imgur.com/Kd3NUMH.png)

We know we need to pass the pool:

![](https://i.imgur.com/mKpaA1a.png)

We know the order of parameters, is just which "data" to hex encode?

![image](https://user-images.githubusercontent.com/12489182/225366857-e165164a-481a-42e8-acec-f3e5ccd09b62.png)

Let's check a pool contract for a swap function:

![](https://i.imgur.com/TUAaHPf.png)

### Keyword: unwrapBento

![](https://i.imgur.com/JlMP5jj.png)
![](https://i.imgur.com/bJbXjtl.png)

- if True (1) call Bento's withdraw function (pull token to an external address)
- else if False (0), call transfer to move tokens within Bento, such as to another Trident pool, or Bento account.

---

So now we know what to pass in the pool data:

- The token in, is fairly clear.
- The recipient, will either be the next pool in the swap, the account in Bentobox (your address), or could be the Trident address if needing to unwrap the gas token after. 
- unwrapBento, we just went through but as an example, if to another pool or your account in Bento, will be 0:

![](https://i.imgur.com/2KdluZb.png)

If to Trident to be unwrapped, from bento, then a 1:

![](https://i.imgur.com/K80Nvl1.png)

In our latter example we are pulling to Trident so we can unwrap some wmatic to matic, or "ETH" as universily used for the gas coin, so as not to change contracts across deployments.

![](https://i.imgur.com/5UQcBbb.png)

To make a batch call we use the multicall feature, but let's look first at the second encoded data we will need to pass it.

![](https://i.imgur.com/zzsffEk.png)

In this example I can use 0, but in order to be safe you should work out a number you are happy with. 
Might be the exact amount out if called from a contract and that can be known, or the amount from getAmountOut minus a percent slippage, so the same as final amountOutMin value. Is up to you.

![](https://i.imgur.com/vSSSInY.png)

So we encode our swap, unwrap, and then finally a list or array of the swap and unwrap calls, with a multicall.

![](https://i.imgur.com/WvhF57E.png)
![](https://i.imgur.com/x53Eog6.png)

![](https://i.imgur.com/Un5PfSL.png)
