from os import getenv
from dotenv import load_dotenv
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
POA_LIST = ['GOERLI', 'POLYGON', 'BSC', 'METIS']
def con(_node: str) -> object:
  load_dotenv()
  w3 = Web3(HTTPProvider(getenv(_node)))
  if _node in POA_LIST:
    w3.middleware_onion.inject(
      geth_poa_middleware,
      layer=0
    )
  return w3
