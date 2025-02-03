import * as anchor from "@coral-xyz/anchor";

const provider = anchor.AnchorProvider.local();
anchor.setProvider(provider);

const program = anchor.workspace.SolanaDataStorage;
const storageAccount = anchor.web3.Keypair.generate();

(async () => {
  // Initialize storage with a value of 42
  await program.rpc.initialize(new anchor.BN(42), {
    accounts: {
      storage: storageAccount.publicKey,
      user: provider.wallet.publicKey,
      systemProgram: anchor.web3.SystemProgram.programId,
    },
    signers: [storageAccount],
  });

  console.log(
    "Storage account initialized:",
    storageAccount.publicKey.toBase58()
  );

  // Update the stored value to 100
  await program.rpc.updateValue(new anchor.BN(100), {
    accounts: {
      storage: storageAccount.publicKey,
    },
  });

  console.log("Updated value to 100");
})();