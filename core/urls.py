from django.urls import path
from .views import AboutView, IndexDashboardView


app_name="core"

urlpatterns = [
     path("about/", AboutView.as_view(), name="about"),
     path("", IndexDashboardView.as_view(), name="index"),
]
