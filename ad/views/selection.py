from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ad.models import Selection
from ad.permissions import IsSelectionOwner
from ad.serializers import SelectionSerializer, SelectionDetailSerializer, SelectionListSerializer, \
    SelectionCreateSerializer


class SelectionViewSet(ModelViewSet):
    queryset = Selection.objects.all()
    default_serializer = SelectionSerializer
    serializer_classes = {
        "list": SelectionListSerializer,
        "retrieve": SelectionDetailSerializer,
        "create": SelectionCreateSerializer
    }
    default_permissions = [AllowAny()]
    permissions = {
        "create": [IsAuthenticated()],
        "retrieve": [IsAuthenticated()],
        "update": [IsAuthenticated(), IsSelectionOwner()],
        "partial_update": [IsAuthenticated(), IsSelectionOwner()],
        "delete": [IsAuthenticated(), IsSelectionOwner()],

    }

    def get_permissions(self):
        return self.permissions.get(self.action, self.default_permissions)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer)