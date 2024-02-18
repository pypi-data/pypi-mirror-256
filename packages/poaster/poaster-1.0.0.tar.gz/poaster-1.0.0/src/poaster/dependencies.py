from collections.abc import AsyncGenerator

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from poaster.access import repository
from poaster.core import exceptions, http_exceptions, oauth, sessions

AuthBearer = Annotated[oauth.Token, Depends(oauth.oauth2_scheme)]
AuthForm = Annotated[OAuth2PasswordRequestForm, Depends()]


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session, commiting changes before closing."""
    async with sessions.async_session() as session:
        yield session
        await session.commit()


Session = Annotated[AsyncSession, Depends(get_session)]


def get_user_repository(session: Session) -> repository.SqlalchemyUserRepository:
    """Instantiate user repository session."""
    return repository.SqlalchemyUserRepository(session)


UserRepository = Annotated[
    repository.SupportsUserRepository, Depends(get_user_repository)
]


def get_current_username(token: AuthBearer) -> str:
    """Try and retrieve username based on passed token."""
    try:
        payload = oauth.decode_token(token)
    except exceptions.Unauthorized as err:
        raise http_exceptions.InvalidCredentials from err
    else:
        return str(payload.get("sub", ""))


CurrentUsername = Annotated[str, Depends(get_current_username)]
