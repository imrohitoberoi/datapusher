import uuid
from models import Account, Destination
from schemas import AccountCreate, AccountUpdate, DestinationCreate, DestinationUpdate
from tortoise.exceptions import DoesNotExist


async def create_account(account: AccountCreate):
    new_account = await Account.create(
        email=account.email,
        account_name=account.account_name,
        app_secret_token=uuid.uuid4().hex,
        website=account.website,
    )
    return new_account


async def get_account(account_id: int):
    try:
        return await Account.get(account_id=account_id)
    except DoesNotExist:
        return None


async def update_account(account_id: int, account: AccountUpdate):
    account_to_update = await get_account(account_id)
    if account_to_update:
        if account.account_name is not None:
            account_to_update.account_name = account.account_name
        if account.website is not None:
            account_to_update.website = account.website
        await account_to_update.save()
        return account_to_update
    return None


async def delete_account(account_id: int):
    account_to_delete = await get_account(account_id)
    if account_to_delete:
        await account_to_delete.delete()
        return True
    return False


async def get_all_accounts():
    return await Account.all()


async def create_destination(account_id: int, destination: DestinationCreate):
    account = await get_account(account_id)
    if not account:
        raise DoesNotExist("Account not found")
    new_destination = await Destination.create(
        account_id=account_id,
        url=destination.url,
        http_method=destination.http_method,
        headers=destination.headers,
    )
    return new_destination


async def get_destination(destination_id: int):
    try:
        return await Destination.get(destination_id=destination_id)
    except DoesNotExist:
        return None


async def update_destination(destination_id: int, destination: DestinationUpdate):
    destination_to_update = await get_destination(destination_id)
    if destination_to_update:
        if destination.url is not None:
            destination_to_update.url = destination.url
        if destination.http_method is not None:
            destination_to_update.http_method = destination.http_method
        if destination.headers is not None:
            destination_to_update.headers = destination.headers
        await destination_to_update.save()
        return destination_to_update
    return None


async def delete_destination(destination_id: int):
    destination_to_delete = await get_destination(destination_id)
    if destination_to_delete:
        await destination_to_delete.delete()
        return True
    return False


async def get_all_destinations(account_id: int):
    return await Destination.filter(account_id=account_id)
