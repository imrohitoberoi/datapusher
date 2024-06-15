from tortoise import fields, models
from fastapi import HTTPException
from starlette import status
from constants import HTTP_METHOD_REQUIRED, INVALID_HTTP_METHOD, VALID_HTTP_METHODS


class Account(models.Model):
    """
    Represents an account in the system.
    """
    account_id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    account_name = fields.CharField(max_length=255)
    app_secret_token = fields.CharField(max_length=255, unique=True)
    website = fields.CharField(max_length=255, null=True, blank=True)

    class Meta:
        table = "accounts"

    def __str__(self):
        """
        Returns a string representation of the account.
        """
        return self.account_name


class Destination(models.Model):
    """
    Represents a destination associated with an account.
    """
    destination_id = fields.IntField(pk=True)
    account = fields.ForeignKeyField("models.Account", related_name="destinations")
    url = fields.CharField(max_length=255)
    http_method = fields.CharField(max_length=10)
    headers = fields.JSONField()

    class Meta:
        table = "destinations"

    @classmethod
    async def create(cls, **kwargs):
        http_method = kwargs.get('http_method', None)

        if not http_method:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=HTTP_METHOD_REQUIRED)

        if not cls.validate_http_method(http_method):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=INVALID_HTTP_METHOD)

        return await super().create(**kwargs)

    @classmethod
    def validate_http_method(cls, http_method):
        """
        Validates if the provided HTTP method is valid.

        Args:
            http_method (str): The HTTP method to validate.

        Returns:
            bool: True if the HTTP method is valid, False otherwise.
        """
        return http_method.upper() in VALID_HTTP_METHODS

    def __str__(self):
        """
        Returns a string representation of the destination URL.
        """
        return self.url
