# Example xSwap from Polygon to Fantom. - Focused on cook data, assumes wmatic and regular token approval with bentobox.

from eth_abi import encode
from eth_abi.packed import encode_packed
from hexbytes import HexBytes

XSWAP_ADDRESS = '0xd08b5f3e89F1e2d6b067e0A0cbdb094e6e41E77c'
BENTO_ADDRESS = '0x0319000133d3AdA02600f0875d2cf03D442C3367'
V2ROUTER_ADDRESS = '0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506'

USDC_ADDRESS = '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174'
WMATIC_ADDRESS = '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270'
ONE_ETH = 1*10**18

XSWAP_ABI = '''
[{"inputs":[{"internalType":"contract IBentoBoxMinimal","name":"_bentoBox","type":"address"},{"internalType":"contract IStargateRouter","name":"_stargateRouter","type":"address"},{"internalType":"address","name":"_factory","type":"address"},{"internalType":"bytes32","name":"_pairCodeHash","type":"bytes32"},{"internalType":"contract IStargateWidget","name":"_stargateWidget","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"NotStargateRouter","type":"error"},{"inputs":[],"name":"TooLittleReceived","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"srcContext","type":"bytes32"},{"indexed":false,"internalType":"bool","name":"failed","type":"bool"}],"name":"StargateSushiXSwapDst","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"srcContext","type":"bytes32"}],"name":"StargateSushiXSwapSrc","type":"event"},{"inputs":[{"internalType":"contract IERC20","name":"token","type":"address"}],"name":"approveToStargateRouter","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"bentoBox","outputs":[{"internalType":"contract IBentoBoxMinimal","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint8[]","name":"actions","type":"uint8[]"},{"internalType":"uint256[]","name":"values","type":"uint256[]"},{"internalType":"bytes[]","name":"datas","type":"bytes[]"}],"name":"cook","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"uint8","name":"_functionType","type":"uint8"},{"internalType":"address","name":"_receiver","type":"address"},{"internalType":"uint256","name":"_gas","type":"uint256"},{"internalType":"uint256","name":"_dustAmount","type":"uint256"},{"internalType":"bytes","name":"_payload","type":"bytes"}],"name":"getFee","outputs":[{"internalType":"uint256","name":"a","type":"uint256"},{"internalType":"uint256","name":"b","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pairCodeHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"","type":"uint16"},{"internalType":"bytes","name":"","type":"bytes"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"_token","type":"address"},{"internalType":"uint256","name":"amountLD","type":"uint256"},{"internalType":"bytes","name":"payload","type":"bytes"}],"name":"sgReceive","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"stargateRouter","outputs":[{"internalType":"contract IStargateRouter","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"stargateWidget","outputs":[{"internalType":"contract IStargateWidget","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"stateMutability":"payable","type":"receive"}]
'''
BENTO_ABI = '''
[{"inputs":[{"internalType":"contract IERC20","name":"wethToken_","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"masterContract","type":"address"},{"indexed":false,"internalType":"bytes","name":"data","type":"bytes"},{"indexed":true,"internalType":"address","name":"cloneAddress","type":"address"}],"name":"LogDeploy","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"contract IERC20","name":"token","type":"address"},{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"share","type":"uint256"}],"name":"LogDeposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"borrower","type":"address"},{"indexed":true,"internalType":"contract IERC20","name":"token","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"feeAmount","type":"uint256"},{"indexed":true,"internalType":"address","name":"receiver","type":"address"}],"name":"LogFlashLoan","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"protocol","type":"address"}],"name":"LogRegisterProtocol","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"masterContract","type":"address"},{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"LogSetMasterContractApproval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"contract IERC20","name":"token","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"LogStrategyDivest","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"contract IERC20","name":"token","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"LogStrategyInvest","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"contract IERC20","name":"token","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"LogStrategyLoss","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"contract IERC20","name":"token","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"LogStrategyProfit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"contract IERC20","name":"token","type":"address"},{"indexed":true,"internalType":"contract IStrategy","name":"strategy","type":"address"}],"name":"LogStrategyQueued","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"contract IERC20","name":"token","type":"address"},{"indexed":true,"internalType":"contract IStrategy","name":"strategy","type":"address"}],"name":"LogStrategySet","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"contract IERC20","name":"token","type":"address"},{"indexed":false,"internalType":"uint256","name":"targetPercentage","type":"uint256"}],"name":"LogStrategyTargetPercentage","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"contract IERC20","name":"token","type":"address"},{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"share","type":"uint256"}],"name":"LogTransfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"masterContract","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"LogWhiteListMasterContract","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"contract IERC20","name":"token","type":"address"},{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"share","type":"uint256"}],"name":"LogWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes[]","name":"calls","type":"bytes[]"},{"internalType":"bool","name":"revertOnFail","type":"bool"}],"name":"batch","outputs":[{"internalType":"bool[]","name":"successes","type":"bool[]"},{"internalType":"bytes[]","name":"results","type":"bytes[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"contract IBatchFlashBorrower","name":"borrower","type":"address"},{"internalType":"address[]","name":"receivers","type":"address[]"},{"internalType":"contract IERC20[]","name":"tokens","type":"address[]"},{"internalType":"uint256[]","name":"amounts","type":"uint256[]"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"batchFlashLoan","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"claimOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"masterContract","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"bool","name":"useCreate2","type":"bool"}],"name":"deploy","outputs":[{"internalType":"address","name":"cloneAddress","type":"address"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"token_","type":"address"},{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"share","type":"uint256"}],"name":"deposit","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"shareOut","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"contract IFlashBorrower","name":"borrower","type":"address"},{"internalType":"address","name":"receiver","type":"address"},{"internalType":"contract IERC20","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"flashLoan","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"token","type":"address"},{"internalType":"bool","name":"balance","type":"bool"},{"internalType":"uint256","name":"maxChangeAmount","type":"uint256"}],"name":"harvest","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"masterContractApproved","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"masterContractOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pendingOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"name":"pendingStrategy","outputs":[{"internalType":"contract IStrategy","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"token","type":"address"},{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permitToken","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"registerProtocol","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"address","name":"masterContract","type":"address"},{"internalType":"bool","name":"approved","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"setMasterContractApproval","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"token","type":"address"},{"internalType":"contract IStrategy","name":"newStrategy","type":"address"}],"name":"setStrategy","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"token","type":"address"},{"internalType":"uint64","name":"targetPercentage_","type":"uint64"}],"name":"setStrategyTargetPercentage","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"name":"strategy","outputs":[{"internalType":"contract IStrategy","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"name":"strategyData","outputs":[{"internalType":"uint64","name":"strategyStartDate","type":"uint64"},{"internalType":"uint64","name":"targetPercentage","type":"uint64"},{"internalType":"uint128","name":"balance","type":"uint128"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"token","type":"address"},{"internalType":"uint256","name":"share","type":"uint256"},{"internalType":"bool","name":"roundUp","type":"bool"}],"name":"toAmount","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bool","name":"roundUp","type":"bool"}],"name":"toShare","outputs":[{"internalType":"uint256","name":"share","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"name":"totals","outputs":[{"internalType":"uint128","name":"elastic","type":"uint128"},{"internalType":"uint128","name":"base","type":"uint128"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"token","type":"address"},{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"share","type":"uint256"}],"name":"transfer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"token","type":"address"},{"internalType":"address","name":"from","type":"address"},{"internalType":"address[]","name":"tos","type":"address[]"},{"internalType":"uint256[]","name":"shares","type":"uint256[]"}],"name":"transferMultiple","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"},{"internalType":"bool","name":"direct","type":"bool"},{"internalType":"bool","name":"renounce","type":"bool"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"masterContract","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"whitelistMasterContract","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"whitelistedMasterContracts","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"token_","type":"address"},{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"share","type":"uint256"}],"name":"withdraw","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"shareOut","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]
'''
V2ROUTER_ABI = '''
[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]
'''
from net import con
w3 = con('POLYGON')

xswap = w3.eth.contract(address=XSWAP_ADDRESS, abi=XSWAP_ABI)
bento = w3.eth.contract(address=BENTO_ADDRESS, abi=BENTO_ABI)
v2router = w3.eth.contract(address=V2ROUTER_ADDRESS, abi=V2ROUTER_ABI)

# These are our actions to 'cook' src side:
# // Bento and Token Operations
ACTION_MASTER_CONTRACT_APPROVAL = 0
ACTION_SRC_DEPOSIT_TO_BENTOBOX = 1
ACTION_SRC_TRANSFER_FROM_BENTOBOX = 2
# // Swap Operations
ACTION_LEGACY_SWAP = 7
# // Bridge Operations
ACTION_STARGATE_TELEPORT = 10
## ---------------------------

# setMasterContractApproval
# 'signHash' the keccak of the encoded data - Need address and key for this
from os import getenv
from dotenv import load_dotenv
load_dotenv()
KEY = getenv('TKEY')
EOA = getenv('TRON')
#----------------------

keccak256 = w3.solidity_keccak
CHAIN_ID = 137
EIP191_PREFIX_FOR_EIP712_STRUCTURED_DATA = '\x19\x01'
DOMAIN_SEPARATOR_SIGNATURE_HASH = keccak256(['string'],["EIP712Domain(string name,uint256 chainId,address verifyingContract)"])
APPROVAL_SIGNATURE_HASH = keccak256(['string'],["SetMasterContractApproval(string warning,address user,address masterContract,bool approved,uint256 nonce)"])
DOMAIN_SEPARATOR = w3.keccak(encode(['bytes32', 'bytes32', 'uint256', 'address'],[DOMAIN_SEPARATOR_SIGNATURE_HASH, keccak256(['string'],["BentoBox V1"]), CHAIN_ID, BENTO_ADDRESS]))

user = EOA
masterContract = XSWAP_ADDRESS
approved = True
nonces = bento.functions.nonces(user).call()

digest = keccak256(['bytes'],[
  encode_packed(['string','bytes32','bytes32'],[
    EIP191_PREFIX_FOR_EIP712_STRUCTURED_DATA,
    HexBytes(DOMAIN_SEPARATOR),
    keccak256(['bytes'],[
          encode(['bytes32','bytes32','address','address','bool','uint256'],
        [
          APPROVAL_SIGNATURE_HASH,
          keccak256(['string'],['Give FULL access to funds in (and approved to) BentoBox?']),
          user,
          masterContract,
          approved,
          nonces
      ])
    ])
  ])
])

signer = w3.eth.account.from_key(KEY)
signed = signer.signHash(digest.hex())

# approve xswap contract
#  address user,
#  bool approved,
#  uint8 v,
#  bytes32 r,
#  bytes32 s
approval_data = encode(['address', 'bool', 'uint8', 'bytes32', 'bytes32'],[EOA, True, signed.v, HexBytes(hex(signed.r)), HexBytes(hex(signed.s))])

# deposit to bento
# if we use a value for amount, share will be 0 and vice versa - Look up function in relevent contract if wanting to know more about any given 'action'
#  address token,
#  address to,
#  uint256 amount,
#  uint256 share
deposit_data = encode(['address', 'address', 'uint256', 'uint256'],[WMATIC_ADDRESS, EOA, ONE_ETH, 0])
# Transfer from bento to xswap contract
#  address token,
#  address to,
#  uint256 amount,
#  uint256 share,
#  bool unwrapBento # external transfer
transfer_data = encode(['address','address','uint256','uint256','bool'],[WMATIC_ADDRESS, XSWAP_ADDRESS, 0, bento.functions.toShare(WMATIC_ADDRESS, ONE_ETH,  False).call(), True])

# legacy swap to stablecoin
#  uint256 amountIn,
#  uint256 amountOutMin,
#  address[] memory path,
#  address to,
#  note: if (amountIn == 0) .. amountIn = IERC20(path[0]).balanceOf(address(this));
usdc_out = v2router.functions.getAmountsOut(ONE_ETH, [WMATIC_ADDRESS, USDC_ADDRESS]).call()[1]
multiplier = 0.01 # 1% slippage
AMOUNT_OUT_WITH_SLIPPAGE = usdc_out - round(multiplier * usdc_out)
swap_data = encode(['uint256','uint256','address[]','address'],[0, AMOUNT_OUT_WITH_SLIPPAGE,[WMATIC_ADDRESS, USDC_ADDRESS], XSWAP_ADDRESS])

# bridge
#  uint16 dstChainId; // stargate dst chain id
#  address  token;  //  token  getting  bridged
#  uint256  srcPoolId;  //  stargate  src  pool  id
#  uint256  dstPoolId;  //  stargate  dst  pool  id
#  uint256  amount;  //  amount  to  bridge
#  uint256  amountMin;  //  amount  to  bridge  minimum
#  uint256  dustAmount;  //  native  token  to  be  received  on  dst  chain
#  address  receiver;  //  sushiXswap  on  dst  chain
#  address  to;  //  receiver  bridge  token  incase  of  transaction  reverts  on  dst  chain
#  uint256  gas;  //  extra  gas  to  be  sent  for  dst  chain  operations
#  bytes32  srcContext;  //  random  bytes32  as  source  context
STG_FTM_CHAIN_ID = 112
SRC_POOL = 1
DST_POOL = 1
CONTEXT = HexBytes('0x'+('{:0>64}'.format('ba5edb100ded')))
DST_XSWAP_ADDRESS = '0xD045d27c1f7e7f770a807B0a85d8e3F852e0F2BE'
EXTRA_GAS =  1060000

# payload
#  address to,
#  uint8[] memory actions,
#  uint256[] memory values,
#  bytes[] memory datas,
#  bytes32 srcContext
#  ) = abi.decode(payload, (address, uint8[], uint256[], bytes[], bytes32));
WFTM_ADDRESS = '0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83'
DST_USDC_ADDRESS = '0x04068DA6C83AFCFA0e13ba15A6696662335D5B75'
# destination actions
# legacy swap
REKLESS_SLIPPAGE = 1*10**18 # 20 minute bridge and I can't be assed, if out of range you will just get usdc
dst_swap_data = encode(['uint256','uint256','address[]','address'],[0, REKLESS_SLIPPAGE,[DST_USDC_ADDRESS, WFTM_ADDRESS], DST_XSWAP_ADDRESS])
# unwrap to native
ACTION_UNWRAP_AND_TRANSFER = 6
# (address token, address to)
dst_unrwap_data = encode(['address','address'],[WFTM_ADDRESS, EOA])

dst_actions = [ACTION_LEGACY_SWAP,ACTION_UNWRAP_AND_TRANSFER]
dst_values = [0,0]
dst_datas = [dst_swap_data, dst_unrwap_data]

bridge_data = encode(
  ['uint16','address','uint256','uint256','uint256','uint256','uint256','address','address','uint256','bytes32', 'uint8[]',  'uint256[]', 'bytes[]','bytes'],
  [STG_FTM_CHAIN_ID, USDC_ADDRESS, SRC_POOL, DST_POOL, 0, 0, 0, DST_XSWAP_ADDRESS, EOA, EXTRA_GAS, CONTEXT,dst_actions,dst_values,dst_datas,CONTEXT]
)

# put it together
src_actions = [ACTION_MASTER_CONTRACT_APPROVAL,ACTION_SRC_DEPOSIT_TO_BENTOBOX,ACTION_SRC_TRANSFER_FROM_BENTOBOX,ACTION_LEGACY_SWAP,ACTION_STARGATE_TELEPORT]
src_values = [0,0,0,0,0]
src_datas = [approval_data,deposit_data,transfer_data,swap_data,bridge_data]

calldata = xswap.functions.cook(src_actions, src_values, src_datas)

tx = {
        'from': EOA,
        'value': 4000000000000000000,
        'chainId': 137,
        'gas': 700000,
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

# driver
def main():
  bridge = calldata.build_transaction(tx)
  print ('[-] Attempting... ')
  tx_hash = send_tx(sign_tx(bridge, KEY))
  receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
  print (f'[>] Hash and receipt of attempt: {tx_hash}\n[>] {receipt}')

if __name__ == '__main__':
  main()
