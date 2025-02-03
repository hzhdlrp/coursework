use anchor_lang::prelude::*;

declare_id!("4LKtWMzy9MJ9vTkRv53urecomn5S5FnPQoFZrP8bkQgG");

#[program]
pub mod solana_data_storage {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>, value: u64) -> Result<()> {
        let storage = &mut ctx.accounts.storage;
        storage.value = value;
        Ok(())
    }

    pub fn update_value(ctx: Context<UpdateValue>, new_value: u64) -> Result<()> {
        let storage = &mut ctx.accounts.storage;
        storage.value = new_value;
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(init, payer = user, space = 8 + 8)]
    pub storage: Account<'info, StorageData>,
    #[account(mut)]
    pub user: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct UpdateValue<'info> {
    #[account(mut)]
    pub storage: Account<'info, StorageData>,
}

#[account]
pub struct StorageData {
    pub value: u64,
}