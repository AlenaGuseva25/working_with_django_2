from rest_framework import serializers

from rest_framework.fields import HiddenField
from materials.models import Course, Lesson, Subscription
from .validators import validate_video_link


class LessonSerializer(serializers.ModelSerializer):
    link_to_the_video = serializers.URLField(validators=[validate_video_link])
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    owner = HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    number_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_number_lessons(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        'Проверка подписан ли пользователь на курс'
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False


