from django.template.context_processors import request
from rest_framework import permissions, viewsets, generics
from users.models import MODERATOR_GROUP_NAME


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name=MODERATOR_GROUP_NAME).exists()


class IsOwner(permissions.BasePermission):
    """Доступ только владельцу объекта."""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOwnerOrModerator(permissions.BasePermission):
    """Доступ владельцу или модератору."""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.groups.filter(name=MODERATOR_GROUP_NAME).exists()


class IsNotModerator(permissions.BasePermission):
    """Проверка является ли пользователь не модератором."""
    def has_permission(self, request, view):
        return not request.user.groups.filter(name=MODERATOR_GROUP_NAME).exists()