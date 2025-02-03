import * as anchor from "@project-serum/anchor";
import { Program } from "@project-serum/anchor";
import { solana_new } from "../target/types/MyProject";

const provider = anchor.AnchorProvider.env();
anchor.setProvider(provider);

const program = anchor.workspace.MyProject as Program<solana_new>;

async function main() {
  console.log("Deploying program...");
  await program.methods
    .initialize(new anchor.BN(42))
    .accounts({
      myAccount: anchor.web3.Keypair.generate().publicKey,
      user: provider.wallet.publicKey,
      systemProgram: anchor.web3.SystemProgram.programId,
    })
    .signers([])
    .rpc();

  console.log("Program deployed successfully!");
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});