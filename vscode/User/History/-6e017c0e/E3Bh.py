from django.template.response import SimpleTemplateResponse
from django.views.generic import TemplateView

from gccsite.context_processors import (
    privacy_inscription_list,
    privacy_newsletter_list,
    privacy_stage_list,
    faq_entries_list
)


def error_404_view(request, exception):
    response = SimpleTemplateResponse("pages/404.html")
    response.status_code = 404
    return response


from gccsite.context_processors import my_context_processor


class AboutView(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, *args, **kwargs):
        return {}


class LegalNoticesView(TemplateView):
    template_name = "pages/legal_notices.html"

    def get_context_data(self, *args, **kwargs):
        return {}


class PrivacyMainView(TemplateView):
    template_name = "pages/privacy_main.html"

    def get_context_data(self, *args, **kwargs):
        return {}


class PrivacyInscriptionView(TemplateView):
    template_name = "pages/privacy.html"

    def get_context_data(self, *args, **kwargs):
        return {
            "TITLE": "Collecte et traitement des données relatives à l'inscription au site Girls Can Code!",
            "PRIVACY_LIST": privacy_inscription_list(),
        }


class PrivacyStageView(TemplateView):
    template_name = "pages/privacy.html"

    def get_context_data(self, *args, **kwargs):
        return {
            "TITLE": "Collecte et traitement des données relatives à l'inscription à un stage Girls Can Code!",
            "PRIVACY_LIST": privacy_stage_list(),
        }


class PrivacyNewsletterView(TemplateView):
    template_name = "pages/privacy.html"

    def get_context_data(self, *args, **kwargs):
        return {
            "TITLE": "Collecte et traitement des données relatives à l'inscription à la newsletter Girls Can Code!",
            "PRIVACY_LIST": privacy_newsletter_list(),
        }


class FAQView(TemplateView):
    template_name = "pages/FAQ.html"

    def get_context_data(self, *args, **kwargs):
        return faq_entries_list()
