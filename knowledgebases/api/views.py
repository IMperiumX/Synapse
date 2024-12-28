from rest_framework import viewsets, permissions
from rest_framework.response import Response
from knowledgebases.models import KnowledgeBase
from knowledgebases.api.serializers import KnowledgeBaseSerializer

class KnowledgeBaseViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeBase.objects.all()
    serializer_class = KnowledgeBaseSerializer
    permission_classes = [permissions.IsAuthenticated] # Add more granular permissions as needed

    def get_queryset(self):
        """
        Optionally restrict the list of knowledge bases to those that the user has access to.
        For now, we'll just return all knowledge bases if the user is authenticated.
        """
        return KnowledgeBase.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
