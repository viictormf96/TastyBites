from django.urls import path
from .views import IndexDashboardView


app_name="recipes"

urlpatterns = [
    path("", IndexDashboardView.as_view(), name="index"),
]
