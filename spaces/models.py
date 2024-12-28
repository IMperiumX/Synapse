from django.db import models


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
