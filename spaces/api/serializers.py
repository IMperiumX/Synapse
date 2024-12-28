from rest_framework import serializers
from django.contrib.auth.models import Group
from spaces.models import Space, SpacePermission
from users.api.serializers import UserSerializer  # Assuming you have a UserSerializer

class SpacePermissionSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), allow_null=True)

    class Meta:
        model = SpacePermission
        fields = [
            "id",
            "space",
            "user",
            "group",
            "permission_level",
        ]

class SpaceSerializer(serializers.HyperlinkedModelSerializer):
    permissions = SpacePermissionSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Space
        fields = [
            "id",
            "knowledge_base",
            "name",
            "description",
            "parent_space",
            "created_at",
            "updated_at",
            "is_public",
            "permissions",
            "created_by"
        ]

    def validate(self, data):
        """
        Enforce unique constraint: (knowledge_base, name, parent_space).
        """
        knowledge_base = data.get("knowledge_base")
        name = data.get("name")
        parent_space = data.get("parent_space")

        if Space.objects.filter(
            knowledge_base=knowledge_base,
            name=name,
            parent_space=parent_space
        ).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError(
                "A space with this name already exists within the same knowledge base and parent space."
            )
        return data
