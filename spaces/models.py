from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Space(models.Model):
    """
    Represents a logical grouping of pages within a KnowledgeBase (like folders, but more flexible).
    """

    knowledge_base = models.ForeignKey(
        "knowledgebases.KnowledgeBase",
        on_delete=models.CASCADE,
        related_name="spaces",
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    parent_space = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="child_spaces",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)  # Publicly accessible or private

    class Meta:
        unique_together = [
            ("knowledge_base", "name", "parent_space")
        ]  # Spaces must have unique name in the scope of KB/parent_space

    def __str__(self):
        return (
            self.name if not self.parent_space else f"{self.parent_space}/{self.name}"
        )


class SpacePermission(models.Model):
    """
    Defines who has access to a specific space and what they can do.
    """

    class PermissionLevel(models.TextChoices):
        VIEW = "view", _("View")
        EDIT = "edit", _("Edit")
        ADMIN = "admin", _("Admin")

    space = models.ForeignKey(
        Space, on_delete=models.CASCADE, related_name="permissions"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="space_permissions",
    )
    group = models.ForeignKey(
        "auth.Group",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="space_permissions",
    )  # Using Django's built in Group model
    permission_level = models.CharField(max_length=20, choices=PermissionLevel.choices)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(user__isnull=False) | Q(group__isnull=False),
                name="user_or_group_must_be_set_space",
            ),
            models.UniqueConstraint(
                fields=["space", "user"],
                condition=Q(user__isnull=False),
                name="unique_user_space_permission",
            ),
            models.UniqueConstraint(
                fields=["space", "group"],
                condition=Q(group__isnull=False),
                name="unique_group_space_permission",
            ),
        ]

    def __str__(self):
        return f"{self.user or self.group} has {self.permission_level} access to {self.space.name}"
