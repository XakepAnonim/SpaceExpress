from django.urls import path, include

urlpatterns = [
    path("", include("apps.users.urls")),
    path("products/", include("apps.products.urls")),
    path("orders/", include("apps.orders.urls")),
    path("adminka/", include("apps.adminka.urls")),
    path("company/", include("apps.company.urls")),
]
