from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `accounts` ALTER COLUMN `app_secret_token` DROP DEFAULT;
        CREATE TABLE IF NOT EXISTS `destinations` (
    `destination_id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `url` VARCHAR(255) NOT NULL,
    `http_method` VARCHAR(10) NOT NULL,
    `headers` JSON NOT NULL,
    `account_id` INT NOT NULL,
    CONSTRAINT `fk_destinat_accounts_28df5548` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`account_id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `accounts` ALTER COLUMN `app_secret_token` SET DEFAULT '1bbafe44bee54a979be0c22a1d83d6bb';
        DROP TABLE IF EXISTS `destinations`;"""
