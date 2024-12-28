from django.db import models
from django.conf import settings


class EditSession(models.Model):
    """
    Represents an active editing session on a page.
    Used to track who is currently editing a page and coordinate real-time updates.
    """

    page = models.ForeignKey(
        "pages.Page",
        on_delete=models.CASCADE,
        related_name="edit_sessions",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="edit_sessions",
    )
    started_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)  # Updated on each user interaction

    def __str__(self):
        return f"{self.user.username} editing {self.page.title}"
