from typing import Optional

from poaster.bulletin import repository, schemas
from poaster.core import exceptions


async def create_post(
    post_repository: repository.SupportsPostRepository,
    *,
    username: str,
    title: str,
    text: str,
) -> schemas.PostSchema:
    """Create a bulletin post from an authenticated user."""
    post = schemas.PostWithUsernameSchema(title=title, text=text, username=username)
    return await post_repository.create(post)


async def get_post(
    post_repository: repository.SupportsPostRepository, *, id: int
) -> Optional[schemas.PostSchema]:
    """Get a bulletin post by id."""
    try:
        return await post_repository.get_by_id(id)
    except exceptions.DoesNotExist:
        return None


async def get_posts(
    post_repository: repository.SupportsPostRepository,
) -> list[schemas.PostSchema]:
    """Get a bulletin post by id."""
    return await post_repository.get_all()
