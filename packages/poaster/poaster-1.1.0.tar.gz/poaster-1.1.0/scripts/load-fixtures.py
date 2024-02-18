import asyncio
import logging

import poaster.access.repository
import poaster.access.schemas
import poaster.bulletin.repository
import poaster.bulletin.schemas
from poaster.core import exceptions, sessions

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
)


async def load_fixtures():
    """Load test fixtures useful for local development."""
    async with sessions.async_session() as session:
        user_repository = poaster.access.repository.SqlalchemyUserRepository(session)
        post_repository = poaster.bulletin.repository.SqlalchemyPostRepository(session)

        await add_dummy_user(user_repository)
        await add_dummy_posts(post_repository)


async def add_dummy_user(
    user_repository: poaster.access.repository.SupportsUserRepository,
):
    try:
        await user_repository.create(
            poaster.access.schemas.UserLoginSchema(
                username="dummy", password="password"
            )
        )
    except exceptions.AlreadyExists:
        logging.info("'dummy' user already exists with password equal to 'password'.")
    else:
        logging.info("Added 'dummy' user with password equal to 'password'.")


async def add_dummy_posts(
    post_repository: poaster.bulletin.repository.SupportsPostRepository,
):
    async def add_post(title: str, text: str):
        await post_repository.create(
            poaster.bulletin.schemas.PostWithUsernameSchema(
                username="dummy",
                title=title,
                text=text,
            )
        )

    await add_post("Penguins", "Penguins are a group of aquatic flightless birds.")
    await add_post("Tigers", "Tigers are the largest living cat species.")
    await add_post("Koalas", "Koala is is native to Australia.")

    logging.info("Added example dummy posts about animals.")


if __name__ == "__main__":
    asyncio.run(load_fixtures())
