from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, serializers
from materials.paginators import CoursePagination, LessonPagination
from materials.permissions import IsOwner, IsStaff
from materials.models import Course, Lesson, Subscription
from rest_framework.permissions import IsAuthenticated, AllowAny
from materials.serializers import CourseSerializer, LessonSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from materials.services import create_stripe_price, create_stripe_session
from materials.tasks import check_subscribe_course
from users.models import Payments
from users.serializers import PaymentsSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = []
    pagination_class = CoursePagination

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsStaff]
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated, IsOwner|IsStaff]
        elif self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, IsOwner|IsStaff]
        elif self.action == 'update':
            self.permission_classes = [IsAuthenticated, IsOwner|IsStaff]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def perform_update(self, serializer):
        update_course = serializer.save()
        check_subscribe_course.delay(update_course.id)
        update_course.save()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsStaff]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner|IsStaff]
    pagination_class = LessonPagination


class LessonRetrieveView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner|IsStaff]


class LessonUpdateView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner|IsStaff]


class LessonDestroyView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data["course"]
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item, created = Subscription.objects.update_or_create(course=course_item, user=user)

        if created:
            subs_item.status_subscrip = True
            subs_item.save()
            message = 'подписка добавлена'
        # Если подписка у пользователя на этот курс есть - удаляем ее
        elif subs_item.status_subscrip:
            subs_item.status_subscrip = False
            subs_item.save()
            message = 'подписка удалена'

        else:
        # Если подписки у пользователя на этот курс нет - создаем ее
            subs_item.status_subscrip = True
            subs_item.save()
            message = 'подписка добавлена'

        # Возвращаем ответ в API
        return Response({"message": message})


class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        course = serializer.validated_data.get('paid_course')

        if not course:
            raise serializers.ValidationError('Укажите курс')
        payment = serializer.save()

        if course.price != payment.payment_amount:
            raise serializers.ValidationError('Укажите верную цену курса')

        stripe_price_id = create_stripe_price(payment)
        payment.payment_link, payment.payment_id = create_stripe_session(stripe_price_id)

        payment.save()
