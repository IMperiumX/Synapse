from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from spaces.models import Space, SpacePermission
from spaces.api.serializers import SpaceSerializer, SpacePermissionSerializer
from knowledgebases.models import KnowledgeBase

class SpaceViewSet(viewsets.ModelViewSet):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
    permission_classes = [permissions.IsAuthenticated]  # Add more granular permissions

    def get_queryset(self):
        """
        Optionally restrict the list of spaces to those the user has access to.
        """
        user = self.request.user
        # Implement logic to filter spaces based on user permissions
        return Space.objects.all()

    def perform_create(self, serializer):
        knowledge_base_id = self.kwargs.get("knowledge_base_pk")
        knowledge_base = KnowledgeBase.objects.get(pk=knowledge_base_id)
        serializer.save(created_by=self.request.user, knowledge_base=knowledge_base)

class SpacePermissionViewSet(viewsets.ModelViewSet):
    queryset = SpacePermission.objects.all()
    serializer_class = SpacePermissionSerializer
    permission_classes = [permissions.IsAdminUser]  # Adjust as needed

    def get_queryset(self):
        """
        Filter permissions based on space ID.
        """
        space_id = self.kwargs.get("space_pk")
        if space_id:
            return SpacePermission.objects.filter(space_id=space_id)
        return SpacePermission.objects.all()
