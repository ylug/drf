from django.urls import path
from materials.apps import MaterialsConfig
from rest_framework.routers import DefaultRouter

from materials.views import CourseViewSet, LessonCreateAPIView, LessonDestroyView, LessonListAPIView, LessonRetrieveView, LessonUpdateView, PaymentCreateView, SubscriptionView

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')


urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/', LessonRetrieveView.as_view(), name='lesson-get'),
    path('lesson/<int:pk>/update/', LessonUpdateView.as_view(), name='lesson-update'),
    path('lesson/<int:pk>/delete/', LessonDestroyView.as_view(), name='lesson-delete'),
    path('subscription/', SubscriptionView.as_view(),name='subscription'),
    path('payment/create/', PaymentCreateView.as_view(), name='payment_create'),
] + router.urls
