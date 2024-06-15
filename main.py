from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist
from schemas import AccountCreate, AccountUpdate, AccountResponse, DestinationCreate, DestinationUpdate, DestinationResponse
import operations
import config

app = FastAPI()

# Accounts endpoints
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


# Destination endpoints
@app.post("/accounts/{account_id}/destinations/", response_model=DestinationResponse)
async def create_destination(account_id: int, destination: DestinationCreate):
    try:
        new_destination = await operations.create_destination(account_id, destination)
        return new_destination
    except DoesNotExist as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/destinations/{destination_id}", response_model=DestinationResponse)
async def read_destination(destination_id: int):
    destination = await operations.get_destination(destination_id)
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    return destination


@app.put("/destinations/{destination_id}", response_model=DestinationResponse)
async def update_destination(destination_id: int, destination: DestinationUpdate):
    updated_destination = await operations.update_destination(destination_id, destination)
    if not updated_destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    return updated_destination


@app.delete("/destinations/{destination_id}")
async def delete_destination(destination_id: int):
    success = await operations.delete_destination(destination_id)
    if not success:
        raise HTTPException(status_code=404, detail="Destination not found")
    return {"message": "Destination deleted successfully"}


@app.get("/accounts/{account_id}/destinations/", response_model=list[DestinationResponse])
async def read_destinations(account_id: int):
    destinations = await operations.get_all_destinations(account_id)
    return destinations


register_tortoise(
    app,
    config=config.TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
