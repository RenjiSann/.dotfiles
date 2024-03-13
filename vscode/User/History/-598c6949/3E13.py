from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic import TemplateView, View

from .forms import EventApplicationForm
from .models import APPLICATION_STATUS, Application

from events.models import Event
from users.models import User


class ApplicationsView(LoginRequiredMixin, TemplateView):
    template_name = "applications/my_applications.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        user_applications = Application.objects.filter(
            user=self.request.user.id
        ).order_by("-created_at")

        ctx["applications"] = user_applications

        ctx["form"] = EventApplicationForm
        ctx.update(APPLICATION_STATUS)

        return ctx


class ApplicationCreateView(LoginRequiredMixin, View):
    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        redirect_url = request.META.get("HTTP_REFERER", None)
        if not redirect_url:
            redirect_url = reverse("events:home")

        if "submit-application" in request.POST:
            form = EventApplicationForm(request.POST)

            if not form.is_valid():
                messages.warning(
                    request,
                    str(form.errors),
                )
                return HttpResponseRedirect(redirect_url)
            else:
                event = Event.objects.get(id=request.POST["event-id"])
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

                application = Application.objects.create(
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

                return HttpResponseRedirect(redirect_url)

    def http_method_not_allowed(self, request, *args, **kwargs):
        raise Http404()
