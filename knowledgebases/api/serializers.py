from rest_framework import serializers
from knowledgebases.models import KnowledgeBase
from users.api.serializers import UserSerializer  # Assuming you have a UserSerializer

class KnowledgeBaseSerializer(serializers.HyperlinkedModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = KnowledgeBase
        fields = [
            "id",
            "name",
            "description",
            "owner",
            "created_at",
            "updated_at",
            "is_public",
        ]

    def validate_name(self, value):
        """
        Ensure that the knowledge base name is unique (case-insensitive).
        """
        if KnowledgeBase.objects.filter(name__iexact=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("A knowledge base with this name already exists.")
        return value
