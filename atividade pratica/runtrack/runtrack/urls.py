from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from cenario_c.views import (
    signup,
    perfil,
    treino,
    evento,
    LoginView
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/signup/', signup),
    path('api/login/', LoginView.as_view()),
    path('api/refresh/', TokenRefreshView.as_view()),

    path('api/perfil/', perfil),
    path('api/treino/', treino),
    path('api/evento/', evento),
]