import asyncio
import logging

from poaster.access import repository, schemas
from poaster.core import exceptions, sessions

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
)


async def load_fixtures():
    """Load test fixtures useful for local development."""
    async with sessions.async_session() as session:
        user_repository = repository.SqlalchemyUserRepository(session)
        await add_dummy_user(user_repository)


async def add_dummy_user(user_repository: repository.SupportsUserRepository):
    try:
        await user_repository.create(
            schemas.UserLoginSchema(username="dummy", password="password")
        )
    except exceptions.AlreadyExists:
        logging.info("'dummy' user already exists with password equal to 'password'.")
    else:
        logging.info("Added 'dummy' user with password equal to 'password'.")


if __name__ == "__main__":
    asyncio.run(load_fixtures())
