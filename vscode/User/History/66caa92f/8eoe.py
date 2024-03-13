from typing import Any, Dict

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView

from .models import Partner

import structlog
logger = structlog.get_logger(__name__)

class PartnersView(ListView):
    model = Partner
    template_name = "partners/partners_page.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        logger.warning("loading")
        ctx["partners"] = Partner.objects.filter().order_by("status")
        logger.warning("loaded")
        return ctx

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        logger.warning("start dispatch")
        res = super().dispatch(request, *args, **kwargs)
        logger.warning(f"end dispatch:{res}")
        logger.warning(f"rendering:{res}")
        res.render()
        logger.warning(f"rendering done:{res.is_rendered}")
        return res