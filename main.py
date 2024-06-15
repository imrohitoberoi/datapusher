from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import JSONResponse
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist
from schemas import (
    AccountCreate,
    AccountUpdate,
    AccountResponse,
    DestinationCreate,
    DestinationUpdate,
    DestinationResponse
)
import httpx
import operations
import config
from constants import (
    ACCOUNT_DELETED_SUCCESS,
    ACCOUNT_NOT_FOUND,
    DATA_FORWARDED_SUCCESS,
    DESTINATION_DELETED_SUCCESS,
    DESTINATION_NOT_FOUND,
    INVALID_DATA,
    UNAUTHENTICATED
)


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
        raise HTTPException(status_code=404, detail=ACCOUNT_NOT_FOUND)
    return account


@app.put("/accounts/{account_id}", response_model=AccountResponse)
async def update_account(account_id: int, account: AccountUpdate):
    updated_account = await operations.update_account(account_id, account)
    if not updated_account:
        raise HTTPException(status_code=404, detail=ACCOUNT_NOT_FOUND)
    return updated_account


@app.delete("/accounts/{account_id}")
async def delete_account(account_id: int):
    success = await operations.delete_account(account_id)
    if not success:
        raise HTTPException(status_code=404, detail=ACCOUNT_NOT_FOUND)
    return {"message": ACCOUNT_DELETED_SUCCESS}


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
        raise HTTPException(status_code=404, detail=DESTINATION_NOT_FOUND)
    return destination


@app.put("/destinations/{destination_id}", response_model=DestinationResponse)
async def update_destination(destination_id: int, destination: DestinationUpdate):
    updated_destination = await operations.update_destination(destination_id, destination)
    if not updated_destination:
        raise HTTPException(status_code=404, detail=DESTINATION_NOT_FOUND)
    return updated_destination


@app.delete("/destinations/{destination_id}")
async def delete_destination(destination_id: int):
    success = await operations.delete_destination(destination_id)
    if not success:
        raise HTTPException(status_code=404, detail=DESTINATION_NOT_FOUND)
    return { "message": DESTINATION_DELETED_SUCCESS }


@app.get("/accounts/{account_id}/destinations/", response_model=list[DestinationResponse])
async def read_destinations(account_id: int):
    destinations = await operations.get_all_destinations(account_id)
    return destinations


# Data handler endpoint
@app.post("/server/incoming_data")
async def handle_incoming_data(
    request: Request,
    cl_x_token: str = Header(None)
):
    """
    Endpoint to handle incoming data, validate token,
    and forward data to account destinations.
    """
    if cl_x_token is None:
        return JSONResponse(status_code=401, content={ "message": UNAUTHENTICATED })

    account = await operations.get_account_by_token(cl_x_token)
    if not account:
        return JSONResponse(status_code=401, content={ "message": UNAUTHENTICATED })

    try:
        data = await request.json()
    except Exception:
        return JSONResponse(status_code=400, content={ "message": INVALID_DATA })

    destinations = await operations.get_all_destinations(account.account_id)

    async with httpx.AsyncClient() as client:
        for destination in destinations:
            if destination.http_method.lower() == "get":
                response = await client.get(destination.url, params=data, headers=destination.headers)
            else:
                response = await client.request(
                    method=destination.http_method,
                    url=destination.url,
                    json=data,
                    headers=destination.headers,
                )

            if response.status_code >= 400:
                print(f"Failed to send data to {destination.url}: {response.text}")

    return { "message": DATA_FORWARDED_SUCCESS }


register_tortoise(
    app,
    config=config.TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
