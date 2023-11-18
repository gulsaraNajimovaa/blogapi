from typing import List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from app.core.containers import Container
from app.core.dependencies import get_current_user, get_current_superuser
from app.models.users_model import UserModel
from app.schemas.blog_schema import Blog, BaseBlog, EditBlog, EditBlogResponse, SearchBlog, EditTags, EditTagsResponse
from app.services.blog_service import BlogService

blog_router = APIRouter(
    prefix="/blogs",
    tags=["blogs"]
)


@blog_router.post("/create-new-blog", response_model=Blog)
@inject
async def upload_blog(blog: BaseBlog, current_user: UserModel = Depends(get_current_user),
                      service: BlogService = Depends(Provide[Container.blog_service])):
    return service.create(blog)


@blog_router.get("/get-my-blogs", response_model=List[Blog])
@inject
async def get_my_blogs(current_user: UserModel = Depends(get_current_user),
                       service: BlogService = Depends(Provide[Container.blog_service])):
    return service.get_blogs_by_user_id(current_user.id)


@blog_router.patch("/edit-your-blog", response_model=EditBlogResponse)
@inject
async def edit_blog(edit_info: EditBlog, current_user: UserModel = Depends(get_current_user),
                    service: BlogService = Depends(Provide[Container.blog_service])):
    return service.update(current_user.id, schema=edit_info)


@blog_router.delete("/delete-your-blog")
@inject
async def delete_blog(blog_id: int, current_user: UserModel = Depends(get_current_user),
                      service: BlogService = Depends(Provide[Container.blog_service])):
    service.delete(blog_id)
    return "Blog Successfully deleted"


@blog_router.get("/read_", response_model=List[Blog])
@inject
async def read_others_blogs(params: SearchBlog, skip: int = 0, limit: int = 100,
                            current_user: UserModel = Depends(get_current_user),
                            service: BlogService = Depends(Provide[Container.blog_service])):
    return service.search_combined(params, skip, limit)


@blog_router.patch("/edit-tags", response_model=EditTagsResponse)
@inject
async def edit_tags(blog_id: int, edit_info: EditTags,
                    current_user: UserModel = Depends(get_current_user),
                    service: BlogService = Depends(Provide[Container.blog_service])):
    return service.update_blog_tags(blog_id, schema=edit_info)


# for Admin
@blog_router.delete("/admin-delete-blog")
@inject
async def admin_delete_blog(blog_id: int, current_user: UserModel = Depends(get_current_superuser),
                            service: BlogService = Depends(Provide[Container.blog_service])):
    service.delete(blog_id)
    return "Blog Successfully deleted"
