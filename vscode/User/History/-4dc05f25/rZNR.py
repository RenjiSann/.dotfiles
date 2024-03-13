from django.urls import include, path

from . import views

app_name = "events"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("review/", views.ReviewIndexView.as_view(), name="review"),
    path(
        "review/<int:year>/<int:event>",
        views.ApplicationsReviewView.as_view(),
        name="application_review",
    ),
    path(
        "update-application-notes",
        views.ApplicationEditNotesView.as_view(),
        name="update_application_notes",
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
