from django.urls import path

from .views import (
    registration,
    login,
    logout,
    company_application,
)

urlpatterns = [
    path("register", registration),
    path("login", login),
    path("logout", logout),
    path("application", company_application)
]
