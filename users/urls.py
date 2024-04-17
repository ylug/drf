
from django.urls import path
from users.apps import UsersConfig
from users.views import PaymentsListAPIView, UserCreateAPIView, UserDestroyAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = UsersConfig.name


urlpatterns = [
    path('payments/', PaymentsListAPIView.as_view(), name='payments_list'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh_pair'),
    path('user/create/', UserCreateAPIView.as_view(), name='user_create'),
    path('user/list/', UserListAPIView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_detail'),
    path('user/<int:pk>/update/', UserUpdateAPIView.as_view(), name='user_update'),
    path('user/<int:pk>/delete/', UserDestroyAPIView.as_view(), name='user_delete')
]
