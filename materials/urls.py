from django.urls import path

from materials.apps import MaterialsConfig
from rest_framework.routers import DefaultRouter

from materials.views import CourseViewSet, LessonCreateApiView, LessonListView, LessonRetrieveView, LessonUpdateView, \
    LessonDestroyView

app_name = MaterialsConfig.name
router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
                  path('lesson/create/', LessonCreateApiView.as_view(), name='lesson_create'),
                  path('lesson/list/', LessonListView.as_view(), name='lesson_list'),
                  path('lesson/view/<int:pk>/', LessonRetrieveView.as_view(), name='lesson_view'),
                  path('lesson/update/<int:pk>/', LessonUpdateView.as_view(), name='lesson_update'),
                  path('lesson/delete/<int:pk>/', LessonDestroyView.as_view(), name='lesson_delete'),

              ] + router.urls