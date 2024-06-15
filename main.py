from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from schemas import AccountCreate, AccountUpdate, AccountResponse
import operations
import config

app = FastAPI()

@app.post("/accounts/", response_model=AccountResponse)
async def create_account(account: AccountCreate):
    new_account = await operations.create_account(account)
    return new_account


@app.get("/accounts/{account_id}", response_model=AccountResponse)
async def read_account(account_id: int):
    account = await operations.get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@app.put("/accounts/{account_id}", response_model=AccountResponse)
async def update_account(account_id: int, account: AccountUpdate):
    updated_account = await operations.update_account(account_id, account)
    if not updated_account:
        raise HTTPException(status_code=404, detail="Account not found")
    return updated_account


@app.delete("/accounts/{account_id}")
async def delete_account(account_id: int):
    success = await operations.delete_account(account_id)
    if not success:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"message": "Account deleted successfully"}


@app.get("/accounts/", response_model=list[AccountResponse])
async def read_accounts():
    accounts = await operations.get_all_accounts()
    return accounts


register_tortoise(
    app,
    config=config.TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
