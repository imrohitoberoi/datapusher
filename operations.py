import uuid
from models import Account, Destination
from schemas import AccountCreate, AccountUpdate, DestinationCreate, DestinationUpdate
from tortoise.exceptions import DoesNotExist


async def create_account(account: AccountCreate):
    """
    Creates a new account in the database.

    Args:
        account (AccountCreate): Data to create the account.

    Returns:
        Account: Created account object.
    """
    new_account = await Account.create(
        email=account.email,
        account_name=account.account_name,
        app_secret_token=uuid.uuid4().hex,  # Generate a unique token for the new account
        website=account.website,
    )
    return new_account


async def get_account(account_id: int):
    """
    Retrieves an account by its ID.

    Args:
        account_id (int): ID of the account to retrieve.

    Returns:
        Optional[Account]: Account object if found, None if not found.
    """
    try:
        return await Account.get(account_id=account_id)
    except DoesNotExist:
        return None


async def get_account_by_token(app_secret_token: str):
    """
    Retrieves an account by its app secret token.

    Args:
        app_secret_token (str): App secret token of the account to retrieve.

    Returns:
        Optional[Account]: Account object if found, None if not found.
    """
    try:
        return await Account.get(app_secret_token=app_secret_token)
    except DoesNotExist:
        return None


async def update_account(account_id: int, account: AccountUpdate):
    """
    Updates an account's details.

    Args:
        account_id (int): ID of the account to update.
        account (AccountUpdate): Data with fields to update.

    Returns:
        Optional[Account]: Updated account object if successful, None if account does not exist.
    """
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
    """
    Deletes an account.

    Args:
        account_id (int): ID of the account to delete.

    Returns:
        bool: True if account was deleted, False if account does not exist.
    """
    account_to_delete = await get_account(account_id)
    if account_to_delete:
        await account_to_delete.delete()
        return True
    return False


async def get_all_accounts():
    """
    Retrieves all accounts.

    Returns:
        List[Account]: List of all accounts.
    """
    return await Account.all()


async def create_destination(account_id: int, destination: DestinationCreate):
    """
    Creates a new destination associated with an account.

    Args:
        account_id (int): ID of the account to associate the destination with.
        destination (DestinationCreate): Data to create the destination.

    Returns:
        Destination: Created destination object.
    """
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
    """
    Retrieves a destination by its ID.

    Args:
        destination_id (int): ID of the destination to retrieve.

    Returns:
        Optional[Destination]: Destination object if found, None if not found.
    """
    try:
        return await Destination.get(destination_id=destination_id)
    except DoesNotExist:
        return None


async def update_destination(destination_id: int, destination: DestinationUpdate):
    """
    Updates a destination's details.

    Args:
        destination_id (int): ID of the destination to update.
        destination (DestinationUpdate): Data with fields to update.

    Returns:
        Optional[Destination]: Updated destination object if successful, None if destination does not exist.
    """
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
    """
    Deletes a destination.

    Args:
        destination_id (int): ID of the destination to delete.

    Returns:
        bool: True if destination was deleted, False if destination does not exist.
    """
    destination_to_delete = await get_destination(destination_id)
    if destination_to_delete:
        await destination_to_delete.delete()
        return True
    return False


async def get_all_destinations(account_id: int):
    """
    Retrieves all destinations associated with an account.

    Args:
        account_id (int): ID of the account to retrieve destinations for.

    Returns:
        List[Destination]: List of all destinations associated with the account.
    """
    return await Destination.filter(account_id=account_id)
