import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.models import Category, Ad
from ads.permissions import IsAdOwnerOrStaff
from ads.serializers import *


class AdViewSet(ModelViewSet):
    queryset = Ad.objects.order_by("-price")
    default_serializer = AdSerializer
    serializer_classes = {
        "list": AdlistSerializer,
        "retrieve": AdDetailSerializer
    }
    default_permissions = [AllowAny()]
    permissions = {
        "retrieve": [IsAuthenticated()],
        "update": [IsAuthenticated(), IsAdOwnerOrStaff()],
        "partial_update": [IsAuthenticated(), IsAdOwnerOrStaff()],
        "delete": [IsAuthenticated(), IsAdOwnerOrStaff()],
    }

    def get_permissions(self):
        return self.permissions.get(self.action, self.default_permissions)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer)

    def list(self, request, *args, **kwargs):
        categories = request.GET.getlist("cat")
        if categories:
            self.queryset = self.queryset.filter(category_id__in=categories)

        text = request.GET.get("text")
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)

        location = request.GET.get("location")
        if location:
            self.queryset = self.queryset.filter(author__locations__name__icontains=location)

        price_from = request.GET.get("price_from")
        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)

        price_to = request.GET.get("price_to")
        if price_to:
            self.queryset = self.queryset.filter(price_lte=price_to)

        return super().list(request, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class AdUploadImage(UpdateView):
    model = Ad
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES.get('image')
        self.object.save()
        return JsonResponse({"id": self.object.pk,
                             "name": self.object.name,
                             "image": self.object.image.url
                             })