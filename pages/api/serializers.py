from rest_framework import serializers
from django.contrib.auth.models import Group
from pages.models import Page, PageVersion, Attachment, PagePermission
from users.api.serializers import UserSerializer  # Assuming you have a UserSerializer


class AttachmentSerializer(serializers.HyperlinkedModelSerializer):
    uploaded_by = UserSerializer(read_only=True)

    class Meta:
        model = Attachment
        fields = [
            "url",
            "id",
            "page",
            "file",
            "uploaded_by",
            "uploaded_at",
        ]


class PageVersionSerializer(serializers.HyperlinkedModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = PageVersion
        fields = [
            "url",
            "id",
            "page",
            "content",
            "version_number",
            "created_at",
            "created_by",
        ]


class PagePermissionSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), allow_null=True
    )

    class Meta:
        model = PagePermission
        fields = [
            "url",
            "id",
            "page",
            "user",
            "group",
            "permission_level",
        ]


class PageSerializer(serializers.HyperlinkedModelSerializer):
    created_by = UserSerializer(read_only=True)
    last_modified_by = UserSerializer(read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)
    versions = PageVersionSerializer(many=True, read_only=True)
    permissions = PagePermissionSerializer(many=True, read_only=True)


    class Meta:
        model = Page
        fields = [
            "url",
            "id",
            "space",
            "title",
            "content",
            "slug",
            "created_at",
            "updated_at",
            "created_by",
            "last_modified_by",
            "is_public",
            "attachments",
            "versions",
            "permissions",
        ]
        read_only_fields = ["slug"]

    # UNCOMMENT IF YOU WANT TO RETURN HTML INSTEAD OF MARKDOWN
    # def get_content(self, obj):
    #     """
    #     Convert Markdown content to HTML (using a library like 'markdown').
    #     """
    #     import markdown
    #     return markdown.markdown(obj.content)

    def validate(self, data):
        """
        Example of using validate to enforce custom validation rules.
        Here, you could check if a page with the same title already exists in the space.
        """
        space = data.get("space")
        title = data.get("title")
        if space and title:
            if (
                Page.objects.filter(space=space, title=title)
                .exclude(pk=self.instance.pk if self.instance else None)
                .exists()
            ):
                raise serializers.ValidationError(
                    "A page with this title already exists in this space."
                )
        return data
