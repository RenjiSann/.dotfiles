from django.urls import include, path

from . import views

app_name = "applications"

urlpatterns = [
    path(
        "applications",
        views.ApplicationsView.as_view(),
        name="my_applications",
    ),
    path(
        "applications/new",
        views.ApplicationCreateView.as_view(),
        name="create_application",
    ),
    path(
        "applications/status",
        views.ApplicationStatusUpdateView.as_view(),
        name="application_status_update",
    ),
]
