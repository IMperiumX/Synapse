from django.db import models

from django.conf import settings


class KnowledgeBase(models.Model):
    """
    Represents a top-level knowledge base.
    Could be used to separate different knowledge bases for different teams or projects.
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="owned_knowledge_bases",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)  # Publicly accessible or private

    def __str__(self):
        return self.name
