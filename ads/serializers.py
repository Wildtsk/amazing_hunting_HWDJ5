from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from ads.models import Ad, Category, Selection
from ads.validators import not_null
from users.models import User


class AdSerializer(serializers.ModelSerializer):
    is_published = serializers.BooleanField(validators=[not_null], required=False)
    class Meta:
        model = Ad
        fields = "__all__"


class AdDetailSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", queryset=User.objects.all())
    category = SlugRelatedField(slug_field="name", queryset=Category.objects.all())

    class Meta:
        model = Ad
        fields = "__all__"


class AdlistSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", queryset=User.objects.all())
    category = SlugRelatedField(slug_field="name", queryset=Category.objects.all())
    locations = serializers.SerializerMethodField()

    def get_locations(self, ad):
        return [loc.name for loc in ad.author.locations.all()]

    class Meta:
        model = Ad
        fields = "__all__"


class SelectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ["id", "name"]


class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = "__all__"


class SelectionCreateSerializer(serializers.ModelSerializer):
    owner = SlugRelatedField(slug_field="username", queryset=User.objects.all())
    class Meta:
        model = Selection
        fields = "__all__"


class SelectionDetailSerializer(serializers.ModelSerializer):
    owner = SlugRelatedField(slug_field="username", queryset=User.objects.all())
    items = AdlistSerializer(many=True)

    class Meta:
        model = Selection
        fields = "__all__"