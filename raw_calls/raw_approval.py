from os import getenv                                                                                                                                    
from dotenv import load_dotenv                                                                                                                           
from net import con                                                                                                                                      
                                                                                                                                                         
w3 = con()                                                                                                                                               
                                                                                                                                                         
def return_account():                                                                                                                                    
  load_dotenv()                                                                                                                                          
  return { 'addr': getenv('tron'), 'key': getenv('key') }                                                                                                
                                                                                                                                                         
def sign_tx(tx, key):                                                                                                                                    
  return w3.eth.account.sign_transaction(tx, private_key=key)                                                                                                                        
                                                                                                                                                         
def send_tx(signed_tx):                                                                                                                                  
  return w3.eth.send_raw_transaction(signed_tx.rawTransaction)                                                                                                  
                                                                                                                                                         
def main():                                                                                                                                              
  account   = return_account()                                                                                                                             
  nonce     = w3.eth.get_transaction_count(account['addr'])                                                                                                  
  
  function  = '095ea7b3'
  address   = '0000000000000000000000001b02da8cb0d097eb8d57a175b88c7d8b47997506'
  amount    = '0000000000000000000000000000000000000000000000000000000000989680' 
  data      = '0x' + function + address + amount

  tx = {                                                                                                                                                 
    'from'   : account['addr'],                                                                                                                             
    'to'     : '0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270',                                                                                                  
    'value'  : 0,                                                                                                                                           
    'chainId': 137,                                                                                                                                      
    'gas'    : 250000,                                                                                                                                       
    'maxFeePerGas': w3.eth.gas_price * 2,
    'maxPriorityFeePerGas': w3.eth.max_priority_fee * 2,
    'nonce'  : nonce,                                                                                                                                      
    'data'   : data 
  }                                                                                                                                                      
                                                                                                                                                         
  sent = send_tx(sign_tx(tx, account['key']))                                                                                                            
  print (f'hash: {sent}')                                                                                                                                
                                                                                                                                                         
if __name__ == '__main__':                                                                                                                               
  main()                                                                                                                                                 
