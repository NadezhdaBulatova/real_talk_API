"""URL mapping for the user API"""

from django.urls import path 
from user.views import RegisterUserView, RetrieveUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

app_name = 'user'

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('<int:id>/', RetrieveUserView.as_view(), name='user-detail'), 
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]