#!/usr/bin/python3.8
import json
import time
from web3 import Web3
from datetime import datetime
import requests

bsc_url = 'https://bsc-dataseed.binance.org/'
contract = '0x35b182Cbb67688B20a5fc393BEE5e83c1cB4C8c0'

with open('env.json', 'r') as f:
 j = json.load(f)
private_key = j['private_key']

def getabi(contr):
 abi_endpoint = 'https://api.bscscan.com/api?module=contract&action=getabi&address='
 w3_abi = Web3(Web3.HTTPProvider(bsc_url))
 response = requests.get('%s%s'%(abi_endpoint, contr))
 abi_json = json.loads(response.json()['result'])
 return(abi_json)

def sleepuntil(untilts):
 sleepfor = untilts-w3_contract.functions.getTimeStamp().call()
 if sleepfor > 0:
  print('WILL SLEEP UNTIL',str(datetime.fromtimestamp(untilts)))
  time.sleep(sleepfor)
 print(str(datetime.now()))

contract_abi = getabi(contract)
w3 = Web3(Web3.HTTPProvider(bsc_url, request_kwargs={'timeout': 60}))
wallet = w3.eth.account.privateKeyToAccount(private_key)._address
w3_contract = w3.eth.contract(address=w3.toChecksumAddress(contract),abi=contract_abi)
compound_step = w3_contract.functions.COMPOUND_STEP().call()
compound_for_no_tax_withdrawal = w3_contract.functions.COMPOUND_FOR_NO_TAX_WITHDRAWAL().call()
cutoff_step = w3_contract.functions.CUTOFF_STEP().call()
compound_bonus_max_times = w3_contract.functions.COMPOUND_BONUS_MAX_TIMES().call()
counter = 0
while True:
 counter = counter+1
 if counter > 5:
  print('TRIED 5 TIMES AND FAILED CRASHING')
  exit(0)
 userinfo = w3_contract.functions.getUserInfo(w3.toChecksumAddress(wallet)).call()
 #lasthatch timestamp is index 4 lastwithdraw 11
 lasthatch = userinfo[4]
 dailyCompoundBonus = userinfo[9]
 farmerCompoundCount = userinfo[10]
 if farmerCompoundCount < compound_bonus_max_times:
  print('WILL DO COMPOUNDING, COMPOUND COUNTER IS',farmerCompoundCount)
  #autocompound can take place at
  nextinteraction = lasthatch+compound_step
  sleepuntil(nextinteraction)
  nonce = w3.eth.getTransactionCount(wallet)
  tx = w3_contract.functions.hireMoreFarmers(True).buildTransaction({ 'chainId': 56, 'gas': 0, 'gasPrice': w3.eth.gasPrice, 'from': w3.toChecksumAddress(wallet), 'nonce':  nonce })
 else:
  print('WILL DO WITHDRAWAL')
  withdraw_at = lasthatch+cutoff_step
  sleepuntil(withdraw_at)
  nonce = w3.eth.getTransactionCount(wallet)
  tx = w3_contract.functions.sellCrops().buildTransaction({ 'chainId': 56, 'gas': 0, 'gasPrice': w3.eth.gasPrice, 'from': w3.toChecksumAddress(wallet), 'nonce':  nonce })
 gasest = w3.eth.estimateGas(tx)
 tx['gas'] = gasest
 signed_tx =  w3.eth.account.signTransaction(tx, private_key=private_key)
 tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
 print('TX HASH IS',w3.toHex(tx_hash))
 receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)
 if receipt['status'] != 1:
  print('MINED BUT FAILED TRY AGAIN')
  #break
  continue
 print('TX SUCCESSFUL')
 #give time for nodes to catch up, test by nonce increase
 while nonce == w3.eth.getTransactionCount(wallet):
  time.sleep(5)
 print('CONTRACT BALANCE',w3_contract.functions.getBalance().call()*10**-18)
 counter = 0
