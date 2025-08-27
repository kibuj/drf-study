from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import TagViewSet, ResortViewSet

router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'resort', ResortViewSet, basename='resort')

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('', include(router.urls)),
]