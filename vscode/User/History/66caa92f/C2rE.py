from typing import Any, Dict

from django.http import HttpResponse
from django.views.generic import ListView

from .models import Partner

import logging
logger = logging.getLogger(__name__)

class PartnersView(ListView):
    model = Partner
    template_name = "partners/partners_page.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        logger.warning("loading")
        ctx["partners"] = Partner.objects.filter().order_by("status")
        logger.warning("loaded")
        return ctx
