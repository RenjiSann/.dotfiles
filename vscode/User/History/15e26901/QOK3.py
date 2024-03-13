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

from partners.models import Partner
from users.models import User

from .forms import EventSignupForm
from .models import events, signup


class UpdateStatusView(UpdateView):
    http_method_names = ("post",)
    model = signup.Application
    success_url = reverse_lazy("events:my_applications")

    fields = ("status",)

    def get_object(self, *args, **kwargs):
        return signup.Application.objects.get(
            id=self.request.POST["application-id"]
        )


class ApplicationEditNotesView(UpdateView):
    http_method_names = ("post",)
    model = signup.Application

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
        return signup.Application.objects.get(
            id=self.request.POST["application-id"]
        )


class ApplicationEditStatusView(UpdateView):
    http_method_names = ("post",)
    model = signup.Application

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
        return signup.Application.objects.get(
            id=self.request.POST["application-id"]
        )


class HomePageView(ListView):
    model = events.Event
    template_name = "events/home.html"
    form_class = EventSignupForm
    paginate_by = 5

    def post(self, request, *args, **kwargs):
        if "submit-application" in request.POST:
            form = EventSignupForm(request.POST)

            if not form.is_valid():
                messages.warning(
                    request,
                    str(form.errors),
                )
                return HttpResponseRedirect(reverse("events:home"))
            else:
                event = events.Event.objects.get(id=request.POST["event-id"])
                user = User.objects.get(id=request.user.id)

                address = {
                    "street": form.cleaned_data["street_applicant"],
                    "complement": form.cleaned_data["complement_applicant"],
                    "city": form.cleaned_data["city_applicant"],
                    "zip_code": form.cleaned_data["zip_code_applicant"],
                    "country": form.cleaned_data["country_applicant"],
                }

                address_resp = {
                    "street": form.cleaned_data["street_applicant_resp"],
                    "complement": form.cleaned_data[
                        "complement_applicant_resp"
                    ],
                    "city": form.cleaned_data["city_applicant_resp"],
                    "zip_code": form.cleaned_data["zip_code_applicant_resp"],
                    "country": form.cleaned_data["country_applicant_resp"],
                }

                school = {
                    "school_level": form.cleaned_data["school_level"],
                    "name": form.cleaned_data["name_school"],
                    "street": form.cleaned_data["street_school"],
                    "complement": form.cleaned_data["complement_school"],
                    "city": form.cleaned_data["city_school"],
                    "zip_code": form.cleaned_data["zip_code_school"],
                    "country": form.cleaned_data["country_school"],
                }

                form_answer = (
                    {
                        "tshirt": form.cleaned_data["tshirt"],
                        "allergies": form.cleaned_data["allergies"],
                        "diet": form.cleaned_data["diet"],
                        "learning": form.cleaned_data["learn"],
                        "programing": form.cleaned_data["programing"],
                        "studies": form.cleaned_data["studies"],
                        "association": form.cleaned_data["association"],
                    },
                )

                application = signup.Application.objects.create(
                    user=user,
                    first_name=form.cleaned_data["first_name"],
                    last_name=form.cleaned_data["last_name"],
                    dob=form.cleaned_data["birthdate"],
                    email=form.cleaned_data["email"],
                    phone=form.cleaned_data["phone"],
                    address=address,
                    first_name_resp=form.cleaned_data["first_name_resp"],
                    last_name_resp=form.cleaned_data["last_name_resp"],
                    email_resp=form.cleaned_data["email_resp"],
                    phone_resp=form.cleaned_data["phone"],
                    address_resp=address_resp,
                    school=school,
                    event=event,
                    form_answer=form_answer[0],
                    nb_participations=form.cleaned_data["nb_participations"],
                )

                messages.success(
                    request, "Votre candidature a été enregistrée!"
                )

                return HttpResponseRedirect(reverse("events:home"))
        elif "submit-newsletter" in request.POST:
            # TODO : DO SOMETHING HERE ?

            return HttpResponseRedirect(reverse("events:home"))

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        p = Paginator(events.Event.objects.get_open_events(), self.paginate_by)

        page = ctx["page_obj"].number

        try:
            events_list = p.page(page)
        except PageNotAnInteger:
            events_list = p.page(1)
        except EmptyPage:
            events_list = p.page(p.num_pages)

        ctx["paginator"] = p
        ctx["open_events"] = events_list
        ctx["form"] = EventSignupForm

        ctx["partners_avant"] = Partner.objects.filter(status="Promoted")
        ctx["partners_financement"] = Partner.objects.filter(
            status="Financing"
        )
        ctx["partners_accueil"] = Partner.objects.filter(status="Welcoming")

        # Add a list of already applied events if authenticated
        if self.request.user.is_authenticated:
            ctx["already_applied"] = events.Event.objects.filter(
                id__in=signup.Application.objects.filter(
                    user=self.request.user.id
                ).values_list("event", flat=True)
            )

        ctx.update(signup.APPLICATION_STATUS)
        return ctx


class ReviewIndexView(PermissionRequiredMixin, TemplateView):
    permission_required = "users.can_view_applications"
    raise_exception = True
    template_name = "events/application/index.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["years"] = events.Event.objects.years()
        if self.request.GET:
            ctx["events"] = events.Event.objects.filter(
                year=self.request.GET["year"]
            )
        else:
            ctx["events"] = events.Event.objects.get_visible_events()
        ctx.update(signup.APPLICATION_STATUS)
        return ctx


class ApplicationsReviewView(PermissionRequiredMixin, TemplateView):
    permission_required = "users.can_view_applications"
    template_name = "events/application/review.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["applications"] = signup.Application.objects.get_applicants(
            kwargs["event"]
        )
        ctx.update(signup.APPLICATION_STATUS)
        return ctx


class ApplicationsView(LoginRequiredMixin, TemplateView):
    template_name = "events/my_applications.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        user_applications = signup.Application.objects.filter(
            user=self.request.user.id
        ).order_by("-created_at")
        ctx["applications"] = user_applications

        ctx["form"] = EventSignupForm
        ctx.update(signup.APPLICATION_STATUS)
        return ctx


class EventListViewBase(ListView):
    model = events.Event
    template_name = "events/event_list_page.html"
    # Show 5 elements per page
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = EventSignupForm
        context["passed"] = False
        return context


class EventListView(EventListViewBase):

    def get_queryset(self):
        qs = super().get_queryset()
        qs_passed = qs.filter(end_date__date__lte=datetime.date.today())
        # All event which are not passed
        # Show the soonest first
        return qs.difference(qs_passed).order_by("start_date")


class PassedEventListView(EventListViewBase):

    def get_queryset(self):
        qs = super().get_queryset()
        qs_passed = qs.filter(end_date__date__lte=datetime.date.today())
        return qs_passed.order_by("-end_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["passed"] = True
        return context
