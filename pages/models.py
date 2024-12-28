from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class Page(models.Model):
    """
    Represents a single page within the knowledge base.
    """

    space = models.ForeignKey(
        "spaces.Space",
        on_delete=models.CASCADE,
        related_name="pages",
    )
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)  # Markdown content
    slug = models.SlugField(
        max_length=255, blank=True
    )  # URL-friendly version of the title
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_pages",
    )
    last_modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="modified_pages",
    )
    is_public = models.BooleanField(default=False)  # Publicly accessible or private

    class Meta:
        unique_together = [("space", "slug")]  # Unique slug within a space

    def save(self, *args, **kwargs):
        """Generate slug on save if not provided."""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class PageVersion(models.Model):
    """
    Represents a historical version of a page's content.
    """

    page = models.ForeignKey(
        "pages.Page",
        on_delete=models.CASCADE,
        related_name="versions",
    )
    content = models.TextField(blank=True)  # Markdown content at this version
    version_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="page_versions",
    )

    class Meta:
        unique_together = ("page", "version_number")
        ordering = [
            "page",
            "-version_number",
        ]  # Order by page, then descending version number

    def __str__(self):
        return f"{self.page.title} - Version {self.version_number}"


class PagePermission(models.Model):
    """
    Defines who has access to a specific page and what they can do.
    """

    class PermissionLevel(models.TextChoices):
        VIEW = "view", _("View")
        EDIT = "edit", _("Edit")
        ADMIN = "admin", _("Admin")

    page = models.ForeignKey(
        "pages.Page",
        on_delete=models.CASCADE,
        related_name="permissions",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="page_permissions",
    )
    group = models.ForeignKey(
        "auth.Group",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="page_permissions",
    )  # Using Django's built in Group model
    permission_level = models.CharField(max_length=20, choices=PermissionLevel.choices)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(user__isnull=False) | Q(group__isnull=False),
                name="user_or_group_must_be_set",
            ),
            models.UniqueConstraint(
                fields=["page", "user"],
                condition=Q(user__isnull=False),
                name="unique_user_page_permission",
            ),
            models.UniqueConstraint(
                fields=["page", "group"],
                condition=Q(group__isnull=False),
                name="unique_group_page_permission",
            ),
        ]

    def __str__(self):
        return f"{self.user or self.group} has {self.permission_level} access to {self.page.title}"
