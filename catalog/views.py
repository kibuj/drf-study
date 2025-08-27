from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Resort, Tag
from .serializers import ResortSerializer, TagSerializer, RegisterSerializer
from .permissions import CatalogPermission

class RegisterView(APIView):
    permission_classes = [CatalogPermission]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated, CatalogPermission]
    filterset_fields = ["name"]
    search_fields = ["name"]
    ordering_fields = ["name"]

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx

class ResortViewSet(viewsets.ModelViewSet):
    serializer_class = ResortSerializer
    permission_classes = [CatalogPermission, IsAuthenticated]
    filterset_fields = ["location"]  # ?completed=true/false
    ordering_fields = ["created_at", "updated_at"]
    search_fields = ["title", "description"]

    def get_queryset(self):
        return Resort.objects.filter(user=self.request.user).select_related("user").prefetch_related("tags")

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx

