from tortoise import fields, models


class Account(models.Model):
    account_id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    account_name = fields.CharField(max_length=255)
    app_secret_token = fields.CharField(max_length=255, unique=True)
    website = fields.CharField(max_length=255, null=True, blank=True)

    class Meta:
        table = "accounts"

    def __str__(self):
        return self.account_name


class Destination(models.Model):
    destination_id = fields.IntField(pk=True)
    account = fields.ForeignKeyField("models.Account", related_name="destinations")
    url = fields.CharField(max_length=255)
    http_method = fields.CharField(max_length=10)
    headers = fields.JSONField()

    class Meta:
        table = "destinations"

    def __str__(self):
        return self.url
