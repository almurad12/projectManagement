from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from account.views import Register
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from account.views import CustomUserViewSet

router = DefaultRouter()
router.register(r'', CustomUserViewSet, basename='')


urlpatterns = [
    path('login/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',Register,name='register'),
    ##user update
    path('', include(router.urls)),
]