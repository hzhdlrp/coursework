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

load_dotenv()

PROGRAM_ID = PublicKey(os.getenv('SOLANA_PUBKEY'))

SIGNER_KEYPAIR = Keypair.from_secret_key(bytes(json.loads(os.getenv('SOLANA_KEYGEN_PRIVATE'))))

RPC_URL = "https://api.devnet.solana.com"

datas = []
# update_discriminator = hashlib.sha256(b"global:update_value").digest()[:8]
# new_value = 200
# update_schema = CStruct("new_value" / U64)
# datas.append(update_discriminator + update_schema.build({"new_value": new_value}))

get_discriminator = hashlib.sha256(b"global:get_value").digest()[:8]
datas.append(get_discriminator)

async def call_smart_contract():
    async with AsyncClient(RPC_URL) as client:
        for data in datas:
            storage_account = PublicKey(os.getenv('DATA_ACC_KEY'))
            second_signer = Keypair.from_secret_key(bytes.fromhex(os.getenv('SOME_ACC_PRIVATE_KEY')))

            print("Storage Account:", storage_account)
            print("Signer 1:", SIGNER_KEYPAIR.public_key)
            print("Signer 2:", second_signer.public_key)

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

            latest_blockhash_resp = await client.get_latest_blockhash()
            recent_blockhash = latest_blockhash_resp["result"]["value"]["blockhash"]
            transaction.recent_blockhash = recent_blockhash

            transaction.sign(SIGNER_KEYPAIR, second_signer)

            simulate_resp = await client.simulate_transaction(transaction)
            print("Simulation Response:", simulate_resp)

            response = await client.send_raw_transaction(transaction.serialize(), opts=TxOpts(skip_confirmation=False))

            # response = await client.send_transaction(transaction, SIGNER_KEYPAIR, second_signer,
            #                                          opts=TxOpts(skip_confirmation=False))


            print("Response:", response)


asyncio.run(call_smart_contract())
