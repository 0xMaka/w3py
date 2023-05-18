from eth_account import Account
from eth_account.signers.local import LocalAccount
from zksync2.module.module_builder import ZkSyncBuilder

from zksync2.module.module_builder import ZkSyncBuilder
from zksync2.core.types import EthBlockParams

endpoint = 'https://mainnet.era.zksync.io'

zk3 = ZkSyncBuilder.build(endpoint) 

def get_bal(add: str) -> int:
  return zk3.zksync.get_balance(add, EthBlockParams.LATEST.value)

print(get_bal('0x8c14ed4F602ac4d2Be8Ed9c4716307c73e9A83A8'))
