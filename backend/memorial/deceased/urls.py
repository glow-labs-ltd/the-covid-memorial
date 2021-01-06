from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register('deceased', views.DeceasedAPIViewSet, basename='deceased')

urlpatterns = [
    path('', include(router.urls)),
]