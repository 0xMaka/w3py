import requests

def run_query(q):
    request = requests.post('https://api.thegraph.com/subgraphs/name/sushiswap/exchange', json={'query': q})
    if request.status_code == 200:
      return request.json()
    else:
      raise Exception(f'Call failed. Return code: {request.status_code}. \n{query}')

query = '''
{
pair(id: "0xc3d03e4f041fd4cd388c549ee2a29a9e5075882f",
  block: {number:14914285}) {
  token0 {
    symbol
    id
    decimals
  }
  token1{
    symbol
    id
    decimals
  }
  token0Price
  token1Price
  volumeUSD
  }
}
'''

response = run_query(query)

print(f'[+] Result: {response}')
