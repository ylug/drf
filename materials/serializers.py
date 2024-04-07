from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson
from materials.validators import url_validator
from users.models import Subscription


class LessonSerializer(serializers.ModelSerializer):
    """Базовый сериализатор урока"""
    url = serializers.URLField(validators=[url_validator])

    class Meta:
        model = Lesson
        fields = '__all__'


class LessonDetailSerializer(serializers.ModelSerializer):
    """Cериализатор с информацией об уроке, где для курса выводится его наименование"""
    course = SlugRelatedField(slug_field='name', queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    quantity_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(read_only=True, many=True)

    def get_quantity_lessons(self, obj):
        quantity_lessons = obj.lesson.all().count()

        if not quantity_lessons:
            return None
        else:
            return quantity_lessons

    class Meta:
        model = Course
        fields = '__all__'


class CourseDetailSerializer(serializers.ModelSerializer):
    """Сериализатор о курсе, включает поля кол-ва уроков и
    списка уроков"""
    lessons_count = SerializerMethodField()
    lessons_list = SerializerMethodField()
    is_subscribed = SerializerMethodField()

    def user_(self):
        """Получаем текущего пользователя"""
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def get_is_subscribed(self, course):
        return course.subscription_set.filter(user=self.user_()).exists()

        @staticmethod
        def get_lessons_count(course):
            return Lesson.objects.filter(course=course).count()

        @staticmethod
        def get_lessons_list(course):
            return LessonSerializer(Lesson.objects.filter(course=course), many=True).data

        class Meta:
            model = Course
            fields = '__all__'

    class LessonDetailSerializer(serializers.ModelSerializer):
        """Cериализатор для просмотра информации об уроке, где для курса выводится его наименование"""
        course = SlugRelatedField(slug_field='name', queryset=Course.objects.all())

        class Meta:
            model = Lesson
            fields = '__all__'
