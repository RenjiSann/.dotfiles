from django.urls import include, path

from . import views

app_name = "events"

urlpatterns = [
    path(
        "",
        views.ApplicationsView.as_view(),
        name="my_applications",
    ),
    path(
        "events",
        views.EventListView.as_view(),
        name="events",
    ),
    path(
        "events/passed",
        views.PassedEventListView.as_view(),
        name="passed_events",
    ),
]
