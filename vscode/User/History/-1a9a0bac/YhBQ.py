from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("events.urls")),
    path("", include("pages.urls")),
    path("", include("users.urls")),
    path("", include("partners.urls")),
    path("rest/auth/oidc/", include("mozilla_django_oidc.urls")),
    path("newsletter/", include("newsletter.urls"))
]
