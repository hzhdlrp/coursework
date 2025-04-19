from solana.rpc.async_api import AsyncClient
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, Transaction, AccountMeta
from solana.rpc.types import TxOpts
from solana.keypair import Keypair
import asyncio
import hashlib
from borsh_construct import CStruct, U64
import os
from dotenv import load_dotenv
import json
import base64

load_dotenv()

PROGRAM_ID = PublicKey(os.getenv('SOLANA_PUBKEY'))
SIGNER_KEYPAIR = Keypair.from_secret_key(bytes(json.loads(os.getenv('SOLANA_KEYGEN_PRIVATE'))))
RPC_URL = "https://api.devnet.solana.com"
DATA_ACC_KEY = PublicKey(os.getenv("DATA_ACC_KEY"))

update_discriminator = hashlib.sha256(b"global:update_value").digest()[:8]
get_discriminator = hashlib.sha256(b"global:get_value").digest()[:8]

StorageData = CStruct("value" / U64)

async def get_stored_value():
    async with AsyncClient(RPC_URL) as client:
        resp = await client.get_account_info(DATA_ACC_KEY)
        account_data = resp["result"]["value"]

        if not account_data:
            print("Account not found or empty.")
            return None

        encoded_data = account_data["data"][0]  # base64
        raw_data = base64.b64decode(encoded_data)
        decoded = StorageData.parse(raw_data[8:])

        print(f"Stored value: {decoded.value}")
        print(decoded.value)
        return decoded.value

async def call_smart_contract_get():
    return await get_stored_value()

async def call_smart_contract_set(new_value: int):
    update_schema = CStruct("new_value" / U64)
    data = update_discriminator + update_schema.build({"new_value": new_value})

    storage_account = DATA_ACC_KEY
    second_signer = Keypair.from_secret_key(bytes.fromhex(os.getenv('SOME_ACC_PRIVATE_KEY')))

    accounts = [
        AccountMeta(pubkey=storage_account, is_signer=False, is_writable=True),
        AccountMeta(pubkey=SIGNER_KEYPAIR.public_key, is_signer=True, is_writable=True),
        AccountMeta(pubkey=second_signer.public_key, is_signer=True, is_writable=True)
    ]

    instruction = TransactionInstruction(
        keys=accounts,
        program_id=PROGRAM_ID,
        data=data
    )

    transaction = Transaction().add(instruction)
    logs = ""

    async with AsyncClient(RPC_URL) as client:
        latest_blockhash_resp = await client.get_latest_blockhash()
        transaction.recent_blockhash = latest_blockhash_resp["result"]["value"]["blockhash"]

        transaction.sign(SIGNER_KEYPAIR, second_signer)

        simulate_resp = await client.simulate_transaction(transaction)
        print("Simulation Response:", simulate_resp)

        response = await client.send_raw_transaction(transaction.serialize(), opts=TxOpts(skip_confirmation=False))
        print("Response:", response)
        logs = f"Транзакция отправлена: https://solscan.io/tx/{response['result']}?cluster=dev"

    return logs


if __name__ == "__main__":

    print(asyncio.run(call_smart_contract_get()))
#     print(asyncio.run(call_smart_contract_set(42)))
