from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from pages.models import EditSession, Page  # Or from realtime.models import EditSession
from pages.api.serializers import (
    EditSessionSerializer,
)  # Or from realtime.api.serializers import EditSessionSerializer


class EditSessionViewSet(viewsets.ModelViewSet):
    queryset = EditSession.objects.all()
    serializer_class = EditSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter edit sessions based on page ID.
        """
        page_id = self.kwargs.get("page_id")
        if page_id:
            return EditSession.objects.filter(page_id=page_id)
        return EditSession.objects.all()

    def perform_create(self, serializer):
        page_id = self.request.data.get("page")
        page = Page.objects.get(pk=page_id)

        # Check if an active session already exists for this user and page
        existing_session = EditSession.objects.filter(
            page=page, user=self.request.user
        ).first()
        if existing_session:
            # Update last_seen for the existing session
            existing_session.save()  # This will update last_seen due to auto_now=True
            serializer = EditSessionSerializer(existing_session)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Create a new session
            serializer.save(user=self.request.user, page=page)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        # Optionally, handle cleanup when a session is explicitly destroyed
        instance.delete()

    @action(detail=False, methods=["delete"])
    def clear_all(self, request):
        """
        Clears all edit sessions for the current user.
        Useful for handling disconnects or when the user closes the page.
        """
        EditSession.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
