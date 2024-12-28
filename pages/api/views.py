from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from pages.models import Page, PageVersion, Attachment, PagePermission
from pages.api.serializers import (
    PageSerializer,
    PageVersionSerializer,
    AttachmentSerializer,
    PagePermissionSerializer,
)

# Assuming you have a custom permission class like this (you'll need to implement the logic)
# from core.permissions import IsOwnerOrReadOnly, HasObjectPermission
# from rest_framework.permissions import IsAdminUser


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]  # Or your custom permission classes

    # def get_queryset(self):
    #     """
    #     Optionally restrict the list of pages to those that the user has access to.
    #     """
    #     user = self.request.user
    #     # Implement logic to filter pages based on user permissions (see below)
    #     return Page.objects.all()

    # def perform_create(self, serializer):
    #     serializer.save(created_by=self.request.user)

    # def perform_update(self, serializer):
    #     serializer.save(last_modified_by=self.request.user)

    # @action(detail=True, methods=["get"])
    # def versions(self, request, pk=None):
    #     page = self.get_object()
    #     versions = page.versions.all()
    #     serializer = PageVersionSerializer(versions, many=True)
    #     return Response(serializer.data)

    # @action(detail=True, methods=["post"])
    # def create_version(self, request, pk=None):
    #     """
    #     Example of creating a new version manually.
    #     You might integrate this with your OT/CRDT logic.
    #     """
    #     page = self.get_object()
    #     serializer = PageVersionSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(
    #             page=page,
    #             created_by=self.request.user,
    #             version_number=page.versions.count() + 1,
    #         )
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Example of using advanced permissions:
    # def get_permissions(self):
    #     """
    #     Instantiates and returns the list of permissions that this view requires.
    #     """
    #     if self.action == 'list':
    #         permission_classes = [permissions.IsAuthenticated]
    #     elif self.action == 'create':
    #         permission_classes = [permissions.IsAuthenticated]
    #     elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
    #         permission_classes = [HasObjectPermission] # Or your custom object-level permission class
    #     else:
    #         permission_classes = [permissions.IsAdminUser]
    #     return [permission() for permission in permission_classes]


class PageVersionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PageVersion.objects.all()
    serializer_class = PageVersionSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]  # Or your custom permission classes

    def get_queryset(self):
        """
        Filter versions based on page ID.
        """
        page_id = self.kwargs.get("page_id")  # Assuming you use nested routing
        return PageVersion.objects.filter(page_id=page_id)


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]  # Or your custom permission classes

    def get_queryset(self):
        page_id = self.kwargs.get("page_id")
        return Attachment.objects.filter(page_id=page_id)

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class PagePermissionViewSet(viewsets.ModelViewSet):
    queryset = PagePermission.objects.all()
    serializer_class = PagePermissionSerializer
    permission_classes = [permissions.IsAdminUser]  # Or your custom permission classes
