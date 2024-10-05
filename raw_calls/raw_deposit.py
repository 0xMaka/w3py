from os import getenv                                              
from dotenv import load_dotenv                                     
from net import con                                                
                                                                   
w3 = con()                                                         
                                                                   
def return_account():                                              
  load_dotenv()                                                    
  return { 'addr': getenv('tron'), 'key': getenv('key') }          
                                                                   
def sign_tx(tx, key):                                              
  sig = w3.eth.account.sign_transaction                            
  return sig(tx, private_key=key)                                  
                                                                   
def send_tx(signed_tx):                                            
  w3.eth.send_raw_transaction(signed_tx.rawTransaction)            
  return w3.to_hex(w3.keccak(signed_tx.rawTransaction))            
                                                                   
def main():                                                        
  account = return_account()                                       
  nonce = w3.eth.get_transaction_count(account['addr'])            
                                                                   
  tx = {                                                           
    'from': account['addr'],                                       
    'to': '0x6BEbC4925716945D46F0Ec336D5C2564F419682C',            
    'value': 100000000000000000,                                   
    'chainId': 5,                                                  
    'gas': 250000,                                                 
    'maxFeePerGas': w3.to_wei('200', 'gwei'),                      
    'maxPriorityFeePerGas': w3.to_wei('160', 'gwei'),              
    'nonce': nonce,                                                
    'data': '0x439370b1'                                           
  }                                                                
                                                                   
  print (f'sent: {send_tx(sign_tx(tx, account["key"]))}')          
                                                                   
if __name__ == '__main__':                                         
  main()                                                           