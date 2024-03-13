from django.urls import path

from applications import api, views

app_name = "applications"


urlpatterns = [
    path(
        "applications/",
        views.ApplicationsView.as_view(),
        name="my_applications",
    ),
    path(
        "applications/new/",
        views.ApplicationCreateView.as_view(),
        name="create_application",
    ),
    # Application status update endpoint (POST)
    path(
        "application/<int:appid>/status/",
        views.ApplicationStatusUpdateView.as_view(),
        name="application_status_update",
    ),
    # API routes
    path("rest/applications/<int:id>/status", api.application_status),
    path(
        "rest/applications/<int:id>/transition/<str:transition>",
        api.apply_transition,
    ),
    path(
        "rest/applications/<int:id>/notes",
        api.application_notes,
    ),
]
