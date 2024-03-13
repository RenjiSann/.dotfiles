from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from .forms import EventApplicationForm
from .models import APPLICATION_STATUS, Application


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


class ApplicationCreateView(LoginRequiredMixin, CreateView):
    http_method_names = ("post",)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def http_method_not_allowed(self, request, *args, **kwargs):
        raise Http404()