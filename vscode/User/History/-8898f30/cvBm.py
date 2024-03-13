from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView

from profiles.forms import ProfileCreationForm
from profiles.models import Profile

# Create your views here.


class CreateProfileView(LoginRequiredMixin, CreateView):
    template_name = "profiles/create_profiles.html"
    form_class = ProfileCreationForm
    success_url = reverse_lazy("events:events")  # TODO: Update this

    def post(self, request, *args, **kwargs):
        self.object = None

        form = self.get_form()

        if not form.is_valid():
            messages.warning(
                request,
                str(form.errors),
            )
            return self.form_invalid(form)
        else:
            messages.success(
                request,
                "Votre profil a été enregistré ! Utilisez-le pour vous inscrire à un stage sur cette page !",
            )
            return self.form_valid(form)

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw.update({"user": self.request.user})
        return kw


class ProfileListView(LoginRequiredMixin, ListView):
    template_name = "profiles/profiles_list.html"
    model = Profile

    def get_queryset(self):
        profiles = super().get_queryset().filter(user_id=self.request.user.id)
        return profiles


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "profiles/profiles_detail.html"

    def dispatch(self, request, *args, **kwargs):

        profile_id = self.kwargs.get("pk")
        profile = Profile.objects.get(id=profile_id)

        if request.user != profile.user:
            return HttpResponseForbidden()

        super().dispatch(request, *args, **kwargs)


class DeleteProfileView(LoginRequiredMixin, View):
    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        redirect_url = reverse("profiles:profiles_list")

        profile_id = self.kwargs.get("pk")
        profile = Profile.objects.get(id=profile_id)

        if request.user != profile.user:
            return HttpResponseForbidden()

        if not profile:
            return HttpResponseBadRequest("Bad request")

        profile.delete()

        messages.success(request, "Le profil a été supprimé")
        return HttpResponseRedirect(redirect_url)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return HttpResponseBadRequest("Invalid method")
