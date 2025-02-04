import * as anchor from '@project-serum/anchor';
import { Program } from '@project-serum/anchor';
import { SolanaDataStorage } from '../target/types/solana_data_storage';
import { SystemProgram } from '@solana/web3.js';
import { assert } from 'chai';

describe("solana_data_storage", () => {
  let storageAccount: web3.Keypair;

  beforeEach(async () => {
    storageAccount = new web3.Keypair();
  });

  it("initializes storage account", async () => {
    const initialValue = new BN(100);

    const txHash = await pg.program.methods
      .initialize(initialValue)
      .accounts({
        storage: storageAccount.publicKey,
        user: pg.wallet.publicKey,
        systemProgram: web3.SystemProgram.programId,
      })
      .signers([storageAccount])
      .rpc();

    console.log(`Transaction Hash: ${txHash}`);

    await pg.connection.confirmTransaction(txHash);

    const storageData = await pg.program.account.storageData.fetch(
      storageAccount.publicKey
    );

    console.log("Stored Value:", storageData.value.toString());

    assert(initialValue.eq(storageData.value));
  });

  it("updates the stored value", async () => {
    const initialValue = new BN(50);
    const newValue = new BN(200);

    await pg.program.methods
      .initialize(initialValue)
      .accounts({
        storage: storageAccount.publicKey,
        user: pg.wallet.publicKey,
        systemProgram: web3.SystemProgram.programId,
      })
      .signers([storageAccount])
      .rpc();

    const txHash = await pg.program.methods
      .updateValue(newValue)
      .accounts({
        storage: storageAccount.publicKey,
      })
      .rpc();

    console.log(`Transaction Hash: ${txHash}`);

    await pg.connection.confirmTransaction(txHash);

    const storageData = await pg.program.account.storageData.fetch(
      storageAccount.publicKey
    );

    console.log("Updated Stored Value:", storageData.value.toString());

    assert(newValue.eq(storageData.value));
  });

  it("retrieves the stored value", async () => {
    const provider = anchor.AnchorProvider.env();
    anchor.setProvider(provider);
    const program = anchor.workspace.SolanaDataStorage;

    const storageAccount = new web3.Keypair();
    const initialValue = new BN(42);

    await program.methods
      .initialize(initialValue)
      .accounts({
        storage: storageAccount.publicKey,
        user: provider.wallet.publicKey,
        systemProgram: web3.SystemProgram.programId,
      })
      .signers([storageAccount])
      .rpc();

    const storageData = await program.account.storageData.fetch(
      storageAccount.publicKey
    );

    console.log("Retrieved Stored Value:", storageData.value.toString());

    assert(initialValue.eq(storageData.value));
  });
});
