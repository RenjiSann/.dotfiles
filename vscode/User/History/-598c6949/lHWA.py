from models import Application, APPLICATION_STATUS



class ApplicationsView(LoginRequiredMixin, TemplateView):
    template_name = "applications/my_applications.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        user_applications = Application.objects.filter(
            user=self.request.user.id
        ).order_by("-created_at")
        ctx["applications"] = user_applications

        ctx["form"] = EventSignupForm
        ctx.update(models.APPLICATION_STATUS)
        return ctx