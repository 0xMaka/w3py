from os import getenv

import json

from eth_account.account import Account
from eth_account.signers.local import LocalAccount
from flashbots import flashbot
from web3 import Web3, HTTPProvider
from web3.exceptions import TransactionNotFound
from web3.types import TxParams

from dotenv import load_dotenv
load_dotenv()
from web3.middleware import geth_poa_middleware 


def main(sol_file, contract):
    sender: LocalAccount = Account.from_key(getenv('TKEY'))
    receiver: LocalAccount = Account.from_key(getenv('PKEY'))
    signature: LocalAccount = Account.from_key(getenv('FLASH'))

    w3 = Web3(HTTPProvider(getenv('NODE')))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0) 
    flashbot(w3, signature)



    print(f'[*] Sender account balance: {Web3.fromWei(w3.eth.get_balance(sender.address), "ether")} ETH')
    
    print(f'[*] Compiling contract ->')
    from compiler import compile_contract
    abi, bytecode = compile_contract(sol_file, contract)
   


    def stack(j):
      with open ('contracts.json', 'a') as f:
        json.dump(j, f, indent=2)  
        f.close()
    
    jdict = {'abi':f'{str(abi)}'} 
    stack(jdict)

    print(f'[+] ABI written to contracts.json')
    print(f'[*] Attempting to deploy contract ->')
    

    # build message
    message = 'TESTRELAY: TEST2'.encode('utf-8')

    from padding import pad
    data = pad(message.hex(), 0, 32) 



    # build and sign transactions
    nonce = w3.eth.get_transaction_count(sender.address)

    tx1: TxParams = {
        'to': '',
        'value': w3.toWei(0, 'ether'),
        'gas': 600000,
        'maxFeePerGas': Web3.toWei(50, 'gwei'),
        'maxPriorityFeePerGas': Web3.toWei(40, 'gwei'),
        'nonce': nonce,
        'chainId': 5,
        'type': 2,

        'data': '0x' + bytecode
    }
    tx1_signed = sender.sign_transaction(tx1)
    
    tx2: TxParams = {
        'to': receiver.address,
        'value': w3.toWei(0.004200071000, 'ether'),
        'gas': 25000,
        'maxFeePerGas': Web3.toWei(30, 'gwei'),
        'maxPriorityFeePerGas': Web3.toWei(20, 'gwei'),
        'nonce': nonce + 1,
        'chainId': 5,
        'type': 2,
        'data': '0x' + data
    }
    tx2_signed = sender.sign_transaction(tx2)


    bundle = [
        {'signed_transaction': tx1_signed.rawTransaction},
        {'signed_transaction': tx2_signed.rawTransaction},
    ]



    # send bundle to be executed in the next 5 blocks
    block = w3.eth.block_number

    try:
        sim_result = w3.flashbots.simulate(bundle, block)
        print('[!] Dumping results of simulation:\n', sim_result)
    except Exception as e:
        print('[-] There was a error with your simulation', e)

    results = []
    for target_block in [block + k for k in [1, 2, 3, 4, 5]]:
        results.append(w3.flashbots.send_bundle(bundle, target_block_number=target_block))
        print(f'[*] Bundle sent to miners block: {target_block}')

    # wait for all results
    results[-1].wait()
    try:
        receipt = results[-1].receipts()
        print(f'[+] Bundle was executed block {receipt[0].blockNumber}')
    except TransactionNotFound:
        print('[-] Bundle was not executed')
        return

    print(f'[*] Sender account balance: {Web3.fromWei(w3.eth.get_balance(sender.address), "ether")} ETH')
    print(f'[*] Contract deployed at: {receipt[0].contractAddress}')
    
    jdict = {'Contract_address':f'{receipt[0].contractAddress}'} 
    stack(jdict)

    print('[+] Address written to contracts.json')  
    print('[+] Mission successful. o>')  

if __name__ == '__main__':
    main('MultiCall.sol', 'TestRelay')
