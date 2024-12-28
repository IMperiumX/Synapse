from pages.api import views
from rest_framework import routers
from knowledgebases.api import views as kb_views
from pages.api import views as page_views

from spaces.api import views as space_views
from users.api import views as user_views


router = routers.DefaultRouter()
router.register(
    r"pages",
    views.PageViewSet,
    basename="page",
)
router.register(
    r"users",
    user_views.UserViewSet,
    basename="user",
)
router.register(
    r"kb",
    kb_views.KnowledgeBaseViewSet,
    basename="knowledgebase",
)
router.register(
    r"spaces",
    space_views.SpaceViewSet,
    basename="space",
)
router.register(
    r"permissions",
    space_views.SpacePermissionViewSet,
    basename="permission",
)
router.register(
    r"versions",
    page_views.PageVersionViewSet,
    basename="version",
)

urlpatterns = router.urls

# TODO: handle nested routers after core functionalities
# # Nested routers (if you want URLs like /api/pages/{page_id}/versions/)
# from rest_framework_nested import routers
# pages_router = routers.NestedSimpleRouter(router, r"pages", lookup="page")
# pages_router.register(r"versions", views.PageVersionViewSet, basename="page-version")
# pages_router.register(
#     r"attachments", views.AttachmentViewSet, basename="page-attachmens"
# )
# pages_router.register(
#     r"permissions", views.PagePermissionViewSet, basename="page-permissios"
# )

# urlpatterns = router.urls + pages_router.urls


# # If you're adding EditSessionViewSet to the pages app:
# from rest_framework_nested import routers

# pages_router = routers.NestedSimpleRouter(router, r"pages", lookup="page")
# pages_router.register(
#     r"edit_sessions", page_views.EditSessionViewSet, basename="page-edit-sessios"
# )

# If you have a separate realtime app, register it to the main router
# router.register(r"edit_sessions", realtime_views.EditSessionViewSet)


# # Nested routers for spaces within a knowledge base
# knowledgebases_router = routers.NestedSimpleRouter(
#     router, r"knowledgebases", lookup="knowledge_base"
# )
# knowledgebases_router.register(
#     r"spaces", space_views.SpaceViewSet, basename="knowledgebase-spacs"
# )

# # Nested routers for permissions within a space
# spaces_router = routers.NestedSimpleRouter(
#     knowledgebases_router, r"spaces", lookup="space"
# )
# spaces_router.register(
#     r"permissions", space_views.SpacePermissionViewSet, basename="space-permissios"
# )
