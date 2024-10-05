from net import con; w3 = con('MAINNET') # your set up
from eth_abi import encode

dai = '0x6B175474E89094C44Da98b954EedeAC495271d0F'
spendee = '0x8c14ed4F602ac4d2Be8Ed9c4716307c73e9A83A8'

num = lambda x : int(x,16)
u256 = lambda x : '0x'+encode(['uint256'],[x]).hex()

# mapping (address => uint) public balanceOf;
slot = 2
index = w3.solidity_keccak(['uint256', 'uint256'],[num(spendee), slot]).hex()

diff = { dai: { 'stateDiff': { index: u256(10000*10**18) } } }

data = '0xa9059cbb000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000005a6d66291495590000'

print(
  'With override: \n',
  w3.eth.call({'from': spendee, 'to': dai, 'data': data}, 'latest', diff)
)
print(
  'Without override: \n',
  w3.eth.call({'from': spendee, 'to': dai, 'data': data}, 'latest')
)
