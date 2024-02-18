import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from poaster.access import repository, schemas
from poaster.core import exceptions


@pytest.fixture
def repo(db_session: AsyncSession) -> repository.SqlalchemyUserRepository:
    return repository.SqlalchemyUserRepository(db_session)


@pytest.fixture
def user_creds() -> schemas.UserLoginSchema:
    return schemas.UserLoginSchema(username="bob", password="password")


async def test_create_user_hashes_password(
    repo: repository.SupportsUserRepository, user_creds: schemas.UserRegistrationSchema
):
    db_user = await repo.create(user_creds)
    assert db_user.password != user_creds.password


async def test_can_create_user(
    repo: repository.SupportsUserRepository, user_creds: schemas.UserRegistrationSchema
):
    got = await repo.create(user_creds)
    want = schemas.UserSchema(
        id=got.id,
        username="bob",
        password=got.password,  # dynamically hashed password
    )

    assert got == want


async def test_duplicate_user_raises(
    repo: repository.SupportsUserRepository, user_creds: schemas.UserRegistrationSchema
):
    await repo.create(user_creds)
    with pytest.raises(exceptions.AlreadyExists):
        await repo.create(user_creds)


async def test_user_is_found_by_username(
    db_session: AsyncSession, repo: repository.SupportsUserRepository
):
    qry = "INSERT INTO users (username, password) VALUES ('bob', 'hashedpw');"
    await db_session.execute(text(qry))

    got = await repo.get_by_username("bob")
    want = schemas.UserSchema(
        id=got.id,
        username="bob",
        password="hashedpw",
    )

    assert got == want


async def test_user_is_not_found_by_username(repo: repository.SupportsUserRepository):
    with pytest.raises(exceptions.DoesNotExist):
        await repo.get_by_username("nobody")


async def test_get_all_users(
    db_session: AsyncSession, repo: repository.SupportsUserRepository
):
    qry = "INSERT INTO users (username, password) VALUES ('bob', 'hashedpw');"
    await db_session.execute(text(qry))

    got = await repo.get_all()
    want = [schemas.UserSchema(id=1, username="bob", password="hashedpw")]

    assert got == want


async def test_get_all_users_none_found(repo: repository.SupportsUserRepository):
    got = await repo.get_all()
    want = []

    assert got == want
