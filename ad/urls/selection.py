from django.urls import path
from rest_framework import routers

from ad.views.selection import SelectionViewSet
urlpatterns = []

router = routers.SimpleRouter()
router.register('', SelectionViewSet)

urlpatterns += router.urls