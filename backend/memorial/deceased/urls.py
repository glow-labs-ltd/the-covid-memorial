from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register('deceased', views.DeceasedAPIViewSet, basename='deceased')
router.register('search', views.SearchAPIViewSet, basename='search')
router.register('comment', views.CommentsAPIViewSet, basename='comment')

urlpatterns = [
    path(
        r'comment/<int:deceased_pk>/',
        views.CommentsAPIViewSet.as_view({'get': 'list'}),
        name='comment-list',
    ),
    path('', include(router.urls)),
]
