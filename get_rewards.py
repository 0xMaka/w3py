import net
w3 = net.con()

user = '...'
chef = '0xc2EdaD668740f1aA35E4D8f227fB8E17dcA888Cd'

import snatch
chef_abi = snatch.abi(chef)
contract = w3.eth.contract(address=chef, abi=chef_abi)

pid = 117

start_block = 14997600
end_block = 14997630

def fetch(start_block, end_block):
  for i in range(start_block, end_block):
    rewards_at_block = contract.functions.pendingSushi(pid, user).call(block_identifier=i)
    print(f'reward at block {i}: {rewards_at_block}')

def main(s, n):
  fetch(s, n)

if __name__ == '__main__':
  main(start_block, end_block)