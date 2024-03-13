import csv
from typing import Any

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import views as auth_views
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import (
    default_token_generator as account_activation_token,
)
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
    RedirectURLMixin,
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import EmailValidator
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, resolve_url
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import CreateView, DeleteView, TemplateView
from django.views.generic.edit import UpdateView

from events.models import events, signup

from .forms import (
    AuthLoginForm,
    AuthRegisterForm,
    DeleteUserForm,
    EmailForm,
    GCCPasswordResetForm,
    NotificationsUpdateForm,
    PasswordUpdateForm,
    PersonalInfoForm,
)
from .models import User

# Extra message tags
TAG_PERSONAL_INFO = "personal_info"
TAG_EMAIL = "email"
TAG_PWD = "pwd"


class UserEditView(LoginRequiredMixin, UpdateView):
    http_method_names = ("post",)
    model = User
    fields = (
        "first_name",
        "last_name",
    )

    def get_object(self, *args, **kwargs):
        return User.objects.get(id=self.request.user.id)

    def get_success_url(self):
        return reverse_lazy("users:account_information") + "#personal-info"


class UserEmailEditView(LoginRequiredMixin, UpdateView):
    http_method_names = ("post",)
    model = User
    fields = ("email",)

    def post(self, request, *agrs, **kwargs):
        # Check if the email is valid using the EmailValidator
        email = request.POST["email"]
        email_validator = EmailValidator()

        try:
            email_validator(email)
        except ValidationError:
            messages.warning(
                self.request,
                "L'email est invalide !",
                extra_tags=TAG_EMAIL,
            )
            return HttpResponseRedirect(
                reverse("users:account_information") + "#personal-info"
            )

        # Check if another user already uses the same email address
        try:
            match = User.objects.get(email=email)
            messages.warning(
                self.request,
                "Un utilisateur avec cet email existe déjà !",
                extra_tags=TAG_EMAIL,
            )
            return HttpResponseRedirect(
                reverse("users:account_information") + "#personal-info"
            )
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            user.email = email
            # Update user in the database.
            user.save()

            # Send a message to display
            messages.success(
                request,
                "Informations personnelles mises à jour",
                extra_tags=TAG_EMAIL,
            )

        # Save the updated email for the user
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("users:account_information") + "#personal-info"


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    def get_success_url(self):
        return reverse_lazy("users:account_information") + "#password"


class ExportUsersCSVView(LoginRequiredMixin, View):
    model = User

    def get(self, request):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="users.csv"'

        writer = csv.writer(response)
        writer.writerow(["First Name", "Last Name", "Email"])

        user = User.objects.get(id=self.request.user.id)
        applications = signup.Application.objects.filter(user=user).order_by(
            "-created_at"
        )

        writer.writerow([user.first_name, user.last_name, user.email])

        writer.writerow([])
        writer.writerow(
            [
                "Application first name",
                "Application last name",
                "Application event name",
                "Application status",
                "Application dob",
                "Application phone",
                "Application address",
                "Application school",
                "Application form answer",
                "created at",
            ]
        )

        for application in applications:
            # Add application data to the CSV row
            writer.writerow(
                [
                    application.first_name,
                    application.last_name,
                    application.event,
                    application.status,
                    application.dob,
                    application.phone,
                    application.address,
                    application.school,
                    application.form_answer,
                    application.created_at,
                ]
            )

        return response

    def get_object(self, *args, **kwargs):
        return User.objects.get(id=self.request.user.id)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    http_method_names = ("post",)

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        messages.success(self.request, _("L'utilisateur a été supprimé"))
        return reverse("events:home")

    def delete(self, request, *args, **kwargs):
        # You can add additional checks here if needed before deletion
        return super().delete(request, *args, **kwargs)


class AccountInformationsView(LoginRequiredMixin, TemplateView):
    template_name = "users/AccountInformationsView.html"

    def post(self, request, *agrs, **kwargs):
        personal_info_form = PersonalInfoForm(request.POST)
        email_form = EmailForm(request.POST)
        password_update_form = PasswordUpdateForm(request.POST)
        notifs_update_form = NotificationsUpdateForm(request.POST)

        if "submit-notifications" in request.POST:
            return HttpResponse("Notifs update form valid")

    def get_context_data(self, **kwargs: Any):
        # Get the request user to prefill the forms
        user = User.objects.get(id=self.request.user.id)

        user_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }

        return {
            "personal_info_form": PersonalInfoForm(user_data),
            "email_form": EmailForm(user_data),
            "password_update_form": PasswordUpdateForm(),
            "notifs_update_form": NotificationsUpdateForm(),
            "delete_user_form": DeleteUserForm(),
        }


class LoginView(auth_views.LoginView):
    template_name = "users/login.html"
    form_class = AuthLoginForm
    redirect_authenticated_user = True


class RegisterView(RedirectURLMixin, CreateView):
    template_name = "users/register.html"
    form_class = AuthRegisterForm

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        """
        Like for the Login View, prevent the access of logged users to this page
        """
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return resolve_url(settings.LOGIN_REDIRECT_URL)

    def form_valid(self, form):
        # Save the user instance without committing it to the database yet
        user = form.save(commit=False)
        user.is_active = False  # Set the user's active status to False until they activate their account
        user.save()

        # Send the activation email to the user
        self.send_activation_email(user, form.cleaned_data["email"])

        return self.get_default_redirect_url()

    def send_activation_email(self, user, email):
        current_site = get_current_site(self.request)
        subject = _("Activate your account on Girls Can Code!")
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)

        activation_link = "{0}/activate/{1}/{2}".format(
            current_site, uid, token
        )

        email_from = settings.EMAIL_HOST_USER
        message = _(
            "Bonjour {0},\n Please activate your account using this link: {1}"
        ).format(user.first_name, activation_link)
        send_mail(subject, message, email_from, [email])

    def get_default_redirect_url(self):
        return HttpResponse(
            _("Please check your email to confirm your registration.")
        )


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(
                request,
                _("Your account has been activated. You can now log in."),
            )
            return redirect(
                settings.LOGIN_REDIRECT_URL
            )  # Redirect to the login page or any other desired page
        else:
            messages.error(
                request, _("Activation link is invalid or has expired.")
            )
            return redirect(
                "activation_error"
            )  # Redirect to an error page if activation fails


class GCCPasswordResetView(PasswordResetView):
    template_name = "users/password_reset.html"
    form_class = GCCPasswordResetForm
    email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")


class GCCPasswordResetDoneView(PasswordResetDoneView):
    template_name = "users/password_reset_done.html"


class GCCPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "users/password_reset.html"
    form_class = GCCPasswordResetForm
    email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")
