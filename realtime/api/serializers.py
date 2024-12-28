from rest_framework import serializers
from pages.models import EditSession  # Or from realtime.models import EditSession
from users.api.serializers import UserSerializer

class EditSessionSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = EditSession
        fields = [
            "id",
            "page",
            "user",
            "started_at",
            "last_seen",
        ]
