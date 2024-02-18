from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED

from poaster import dependencies
from poaster.core import http_exceptions

from . import schemas, services

router = APIRouter(tags=["bulletin"])


@router.post(
    "/posts",
    status_code=HTTP_201_CREATED,
    summary="Creates post when passed valid input.",
)
async def handle_create_post(
    payload: schemas.PostInputSchema,
    username: dependencies.CurrentUsername,
    post_repository: dependencies.PostRepository,
) -> schemas.PostSchema:
    """Defines endpoint for creating bulletin posts."""
    return await services.create_post(
        post_repository,
        username=username,
        title=payload.title,
        text=payload.text,
    )


@router.get("/posts", summary="Get all posts.")
async def handle_get_posts(
    post_repository: dependencies.PostRepository,
) -> list[schemas.PostSchema]:
    """Defines endpoint for retrieving all posts."""
    return await services.get_posts(post_repository)


@router.get("/posts/{id}", summary="Get post by id.")
async def handle_get_post(
    id: int,
    post_repository: dependencies.PostRepository,
) -> schemas.PostSchema:
    """Defines endpoint for retrieving a post by its id."""
    if (post := await services.get_post(post_repository, id=id)) is None:
        raise http_exceptions.NotFound

    return post
