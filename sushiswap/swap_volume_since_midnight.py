import requests                                                                          
                                                                                         
def run_query(q):                                                                        
  request = requests.post(                                                               
          'https://api.thegraph.com/subgraphs/name/sushiswap/exchange'                   
          '',                                                                            
          json={'query': query})                                                         
  if request.status_code == 200:                                                         
    return request.json()                                                                
  else:                                                                                  
    raise Exception(f'Query failed. return code is {request.status_code}. {query}') 
                                                                                         
query = '''{                                                                             
  swaps(                                                                                 
    where: {                                                                             
      pair: "0x055475920a8c93cffb64d039a8205f7acc7722d3",                                
      timestamp_gte: 1661130000                                                          
    }                                                                                    
    orderBy: timestamp,                                                                  
    orderDirection: desc                                                                 
  ) {                                                                                    
    amountUSD                                                                            
    transaction {                                                                        
      timestamp                                                                          
    }                                                                                    
  }                                                                                      
}'''                                                                                     
                                                                                         
result = run_query(query)                                                                
n = 0                                                                                    
                                                                                         
for i in result['data']['swaps']:                                                        
  n += float(i['amountUSD'])                                                             
                                                                                         
print(n)        
