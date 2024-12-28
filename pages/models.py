from django.db import models
from django.conf import settings
from django.utils.text import slugify


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
