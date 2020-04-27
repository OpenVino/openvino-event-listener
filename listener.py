from web3 import Web3
import json
import time
import mysql.connector
import os
from hexbytes import HexBytes

contractAddress = '0x52B31871eFF4479ea7a71A12ea087DEbd33B2b01'

w3 = Web3(Web3.WebsocketProvider("wss://rinkeby.infura.io/ws/v3/6d7880a8f4b347ca8953d2715e164241"))

with open("contracts/contract.abi") as abi_file:
    abi = json.load(abi_file)

contract = w3.eth.contract(address=contractAddress, abi=abi)

disconnected = True

print("====== ENV =======")
print("host: " + os.getenv("DATABASE_HOST", default = 'localhost'))
print("user: " + os.getenv("DATABASE_USERNAME", default = 'test'))
print("passwd: " + os.getenv("DATABASE_PASSWORD", default = 'test123'))
print("database: " + os.getenv("DATABASE_NAME", default = 'test123'))
print("")

def handle_event(event):
    global disconnected, w3
    receipt = w3.eth.waitForTransactionReceipt(event['transactionHash'])
    result = contract.events.InsertedRoot().processReceipt(receipt)

    try: 

        if (disconnected):
            
            w3 = Web3(Web3.WebsocketProvider("wss://rinkeby.infura.io/ws/v3/6d7880a8f4b347ca8953d2715e164241"))
            db = mysql.connector.connect(
                host=os.getenv("DATABASE_HOST", default = 'localhost'),
                user=os.getenv("DATABASE_USERNAME", default = 'test'),
                passwd=os.getenv("DATABASE_PASSWORD", default = 'test123'),
                database=os.getenv("DATABASE_NAME", default = 'test_db')
            )
            disconnected = False

        cursor = db.cursor()
        sql = "INSERT INTO roots(root, tx_hash) VALUES (%s,%s)"
        val = [w3.toHex(result[0]['args']['_root']), w3.toHex(result[0]['transactionHash'])]
        cursor.execute(sql, val)
        db.commit()

        print("Inserted into echo database tx " + val[1] + " for root " + val[0])

    except Exception as e:
        disconnected = True
        print(e)

def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
            time.sleep(poll_interval)

block_filter = w3.eth.filter({'fromBlock':'latest', 'address': contractAddress})
log_loop(block_filter, 2)
