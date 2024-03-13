from django.urls import include, path

from . import views

app_name = "events"

urlpatterns = [
    path(
        "applications",
        views.ApplicationsView.as_view(),
        name="my_applications",
    ),
]
