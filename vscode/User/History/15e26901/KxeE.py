import datetime
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import UpdateView

from applications.forms import EventApplicationForm
from applications.models import APPLICATION_STATUS, Application
from partners.models import Partner
from users.models import User

from .models import Event


class UpdateStatusView(UpdateView):
    http_method_names = ("post",)
    model = Application
    success_url = reverse_lazy("applications:my_applications")

    fields = ("status",)

    def get_object(self, *args, **kwargs):
        return Application.objects.get(id=self.request.POST["application-id"])


class ApplicationEditNotesView(UpdateView):
    http_method_names = ("post",)
    model = Application

    fields = ("notes",)

    def get_success_url(self):
        return reverse(
            "events:application_review",
            kwargs={
                "year": self.request.POST["event-year"],
                "event": self.request.POST["event-id"],
            },
        )

    def get_object(self, *args, **kwargs):
        return Application.objects.get(id=self.request.POST["application-id"])


class ApplicationEditStatusView(UpdateView):
    http_method_names = ("post",)
    model = Application

    fields = ("status",)

    def get_success_url(self):
        return reverse(
            "events:application_review",
            kwargs={
                "year": self.request.POST["event-year"],
                "event": self.request.POST["event-id"],
            },
        )

    def get_object(self, *args, **kwargs):
        return Application.objects.get(id=self.request.POST["application-id"])


class HomePageView(ListView):
    model = Event
    template_name = "events/home.html"
    form_class = EventApplicationForm

    def post(self, request, *args, **kwargs):
        if "submit-newsletter" in request.POST:
            # TODO : DO SOMETHING HERE ?

            return HttpResponseRedirect(reverse("events:home"))

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx["open_events"] = Event.objects.get_open_events(5)
        ctx["form"] = EventApplicationForm

        ctx["partners_avant"] = Partner.objects.filter(status="Promoted")
        ctx["partners_financement"] = Partner.objects.filter(
            status="Financing"
        )
        ctx["partners_accueil"] = Partner.objects.filter(status="Welcoming")

        ctx.update(APPLICATION_STATUS)
        return ctx


class ReviewIndexView(PermissionRequiredMixin, TemplateView):
    permission_required = "users.can_view_applications"
    raise_exception = True
    template_name = "events/application/index.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["years"] = Event.objects.years()
        if self.request.GET:
            ctx["events"] = Event.objects.filter(year=self.request.GET["year"])
        else:
            ctx["events"] = Event.objects.get_visible_events()
        ctx.update(APPLICATION_STATUS)
        return ctx


class ApplicationsReviewView(PermissionRequiredMixin, TemplateView):
    permission_required = "users.can_view_applications"
    template_name = "events/application/review.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["applications"] = Application.objects.get_applicants(
            kwargs["event"]
        )
        ctx.update(APPLICATION_STATUS)
        return ctx


class EventListViewBase(ListView):
    model = Event
    template_name = "events/event_list_page.html"
    # Show 5 elements per page
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = EventApplicationForm
        context["passed"] = False
        return context


class EventListView(EventListViewBase):
    def get_queryset(self):
        qs = super().get_queryset()
        qs_passed = qs.filter(end_date__date__lte=datetime.date.today())

        return qs.difference(qs_passed).order_by("end_date")


class PassedEventListView(EventListViewBase):
    def get_queryset(self):
        qs = super().get_queryset()
        qs_passed = qs.filter(end_date__date__lte=datetime.date.today())
        return qs_passed.order_by("-end_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["passed"] = True
        return context
