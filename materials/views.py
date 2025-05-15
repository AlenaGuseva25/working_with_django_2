from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


from materials.models import Course, Lesson, Subscription
from materials.paginators import LessonsPaginator, CoursesPaginator
from materials.serializers import CourseSerializer, LessonSerializer
from users.models import MODERATOR_GROUP_NAME
from users.permissions import IsModerator, IsOwner, IsOwnerOrModerator, IsNotModerator


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursesPaginator

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        permission_map = {
            'create': [IsAuthenticated, IsNotModerator],
            'retrieve': [IsAuthenticated, IsOwnerOrModerator],
            'update': [IsAuthenticated, IsOwnerOrModerator],
            'partial_update': [IsAuthenticated, IsOwnerOrModerator],
            'destroy': [IsAuthenticated, IsOwner],
            'list': [IsAuthenticated],
            'subscribe': [IsAuthenticated],
            'unsubscribe': [IsAuthenticated],

        }
        permissions = permission_map.get(self.action, [IsAuthenticated])
        return [permission() for permission in permissions]


    @action(detail=True, methods=['post'])
    def subscribe(self, request, pk=None):
        'Подписка на курс'
        course = self.get_object()
        if Subscription.objects.filter(user=request.user, course=course).exists():
            return Response({"detail": "Подписка на этот курс уже существует"}, status=status.HTTP_400_BAD_REQUEST)

        Subscription.objects.create(user=request.user, course=course)
        return Response({"detail": "Подписка оформлена"}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def unsubscribe(self, request, pk=None):
        'Удаление подписки'
        course = self.get_object()
        subscription = Subscription.objects.filter(user=request.user, course=course).first()
        if not subscription:
            return Response({"detail": "Невозможно удалить подписку, так как она не существует"}, status=status.HTTP_400_BAD_REQUEST)

        subscription.delete()
        return Response({"detail": "Подписка удалена"}, status=status.HTTP_204_NO_CONTENT)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsNotModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = LessonsPaginator

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name=MODERATOR_GROUP_NAME).exists():
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner, IsNotModerator]

