from rest_framework import permissions
from pages.models import Page
from spaces.models import Space
from knowledgebases.models import KnowledgeBase


class HasKnowledgeBaseAccess(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, KnowledgeBase):
            return obj.is_public or request.user == obj.owner
        if isinstance(obj, Space):
            return (
                obj.knowledge_base.is_public or request.user == obj.knowledge_base.owner
            )
        if isinstance(obj, Page):
            return (
                obj.space.knowledge_base.is_public
                or request.user == obj.space.knowledge_base.owner
            )
        return False


class HasSpaceAccess(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Space):
            return (
                obj.is_public
                or obj.permissions.filter(user=request.user).exists()
                or obj.knowledge_base.owner == request.user
            )
        if isinstance(obj, Page):
            return (
                obj.space.is_public
                or obj.space.permissions.filter(user=request.user).exists()
                or obj.space.knowledge_base.owner == request.user
            )

        return False


class HasPageAccess(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            obj.is_public
            or obj.permissions.filter(user=request.user).exists()
            or obj.space.knowledge_base.owner == request.user
        )
