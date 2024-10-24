
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from authentification.views.compte_view import CustomTokenObtainPairView
from gestion_comptes.views.citoyen_view import CitoyenRegistrationView

app_name = "authentification"
router = DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),

   path('register/citoyen/', CitoyenRegistrationView.as_view({'post': 'create'}), name='citoyen-register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
