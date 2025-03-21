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
initialize_discriminator = hashlib.sha256(b"global:initialize").digest()[:8]
value = 100
initialize_schema = CStruct("value" / U64)
datas.append(initialize_discriminator + initialize_schema.build({"value": value}))


async def call_smart_contract():
    async with AsyncClient(RPC_URL) as client:
        for data in datas:
            storage_account = PublicKey(os.getenv('DATA_ACC_KEY'))
            # print(SIGNER_KEYPAIR.public_key)
            accounts = [
                AccountMeta(pubkey=storage_account, is_signer=False, is_writable=True),  # Теперь правильно!
                AccountMeta(pubkey=SIGNER_KEYPAIR.public_key, is_signer=True, is_writable=True),
            ]

            instruction = TransactionInstruction(
                keys=accounts,
                program_id=PROGRAM_ID,
                data=data
            )

            transaction = Transaction().add(instruction)

            response = await client.send_transaction(transaction, SIGNER_KEYPAIR,
                                                     opts=TxOpts(skip_confirmation=False))

            print("Response:", response)


asyncio.run(call_smart_contract())
