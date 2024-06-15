import uuid
from models import Account
from schemas import AccountCreate, AccountUpdate
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
