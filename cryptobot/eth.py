from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()


SEPOLIA_RPC_URL = os.getenv('RPC_URL')


CONTRACT_ADDRESS = os.getenv('ADDRESS')


CONTRACT_ABI = [
    {
        "inputs": [{"internalType": "int256", "name": "_value", "type": "int256"}],
        "name": "setKey",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getKey",
        "outputs": [{"internalType": "int256", "name": "", "type": "int256"}],
        "stateMutability": "view",
        "type": "function"
    }
]


web3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC_URL))

if not web3.is_connected():
    print("Ошибка: не удалось подключиться к сети Sepolia")
    exit()

print("Успешно подключено к сети Sepolia")


contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)


def read_key(account_address):
    value = contract.functions.getKey().call({'from': account_address})
    print(f"Текущее значение для {account_address}: {value}")
    return value


def write_key(private_key, value):
    account = web3.eth.account.from_key(private_key)
    nonce = web3.eth.get_transaction_count(account.address)

    txn = contract.functions.setKey(value).build_transaction({
        'from': account.address,
        'nonce': nonce,
        'gas': 100000,
        'gasPrice': web3.eth.gas_price
    })

    signed_txn = web3.eth.account.sign_transaction(txn, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print(f"Транзакция отправлена: {web3.to_hex(tx_hash)}")
    logs = f"Транзакция отправлена: sepolia.etherscan.io/tx/{web3.to_hex(tx_hash)}"

    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Транзакция подтверждена. Hash: {receipt.transactionHash.hex()}")
    return logs


if __name__ == "__main__":
    TEST_PRIVATE_KEY = os.getenv('KEY')
    TEST_ADDRESS = os.getenv('WALLET')

    read_key(TEST_ADDRESS)
    write_key(TEST_PRIVATE_KEY, 1)
    read_key(TEST_ADDRESS)


