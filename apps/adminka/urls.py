from django.urls import path

from .views import application_display, accept_application

urlpatterns = [
    path("display", application_display),
    path("accept/<int:pk>", accept_application),
]
