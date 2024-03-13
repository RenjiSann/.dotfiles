from itertools import chain

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, FormMixin, UpdateView

from .forms import (
    ExpenseReportEntryFormSet,
    ExpenseReportEntryWithAccountingFormSet,
    ExpenseReportForm,
    UserBankingInformationForm,
    UserBankingInformationWithValidationForm,
)
from .models import ExpenseReport, UserBankingInformation
from .tasks import expense_report_generate_document

User = get_user_model()


class IndexView(LoginRequiredMixin, ListView):
    template_name = "index.html"

    @method_decorator(transaction.non_atomic_requests)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        qs = ExpenseReport.objects.filter(created_by=self.request.user)
        if "all" not in self.request.GET:
            qs = qs.exclude(state="_closed")
        return qs


class HelpView(LoginRequiredMixin, TemplateView):
    template_name = "help.html"

    @method_decorator(transaction.non_atomic_requests)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class FormsetMixin(FormMixin, SingleObjectMixin):
    formset_initial = {}
    formset_prefix = None

    is_update_view = False

    def get_formset_initial(self):
        return self.formset_initial.copy()

    def get_formset_prefix(self):
        return self.prefix

    def get_formset_class(self):
        return self.formset_class

    def get_formset(self, formset_class=None):
        if formset_class is None:
            formset_class = self.get_formset_class()
        return formset_class(**self.get_formset_kwargs())

    def get_formset_kwargs(self):
        kwargs = {
            "initial": self.get_formset_initial(),
            "prefix": self.get_formset_prefix(),
            "instance": self.object,
        }
        if self.request.method in ("POST", "PUT"):
            kwargs.update(
                {
                    "data": self.request.POST,
                    "files": self.request.FILES,
                }
            )
        return kwargs

    def get(self, request, *args, **kwargs):
        if getattr(self, "is_update_view", False):
            self.object = self.get_object()
        else:
            self.object = None

        return self.render_to_response(
            self.get_context_data(formset=self.get_formset())
        )

    def post(self, request, *args, **kwargs):
        if getattr(self, "is_update_view", False):
            self.object = self.get_object()
        else:
            self.object = None

        form = self.get_form()
        formset = self.get_formset()
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(formset=formset))


class ExpenseReportListView(LoginRequiredMixin, ListView):
    template_name = "expense_report_list.html"

    @method_decorator(transaction.non_atomic_requests)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        if self.request.user.has_perm("expense_report.manage_expensereport"):
            qs = ExpenseReport.objects.all()
        else:
            qs = ExpenseReport.objects.filter(created_by=self.request.user)
        if "all" not in self.request.GET:
            qs = qs.exclude(state="_closed")
        return qs


class ExpenseReportCreateView(FormsetMixin, LoginRequiredMixin, CreateView):
    template_name = "expense_report_create_update.html"
    model = ExpenseReport
    form_class = ExpenseReportForm
    formset_class = ExpenseReportEntryFormSet

    def form_valid(self, *args, **kwargs):
        res = super().form_valid(*args, **kwargs)
        self.object.created_by = self.request.user
        self.object.modified_by = self.request.user
        self.object.save()

        if not self.object.created_by.banking_information.is_complete:
            messages.info(
                self.request,
                "Vos informations bancaires ne sont pas complètes. Pensez à les mettre à jour dans votre profil avant de soumettre votre note de frais.",
            )

        return res


class ExpenseReportUpdateView(FormsetMixin, LoginRequiredMixin, UpdateView):
    template_name = "expense_report_create_update.html"
    form_class = ExpenseReportForm
    is_update_view = True

    def get_queryset(self):
        if self.request.user.has_perm("expense_report.manage_expensereport"):
            return ExpenseReport.objects.all()
        return ExpenseReport.objects.filter(
            created_by=self.request.user, state__in=("draft", "rejected")
        )

    def get_formset_class(self):
        if self.object.state in ("draft", "submitted"):
            return ExpenseReportEntryFormSet
        return ExpenseReportEntryWithAccountingFormSet

    def form_valid(self, *args, **kwargs):
        res = super().form_valid(*args, **kwargs)
        self.object.modified_by = self.request.user

        self.object.save()

        if not self.object.created_by.banking_information.is_complete:
            messages.info(
                self.request,
                "Vos informations bancaires ne sont pas complètes. Pensez à les mettre à jour dans votre profil avant de soumettre votre note de frais.",
            )

        return res


class ExpenseReportDetailView(LoginRequiredMixin, DetailView):
    template_name = "expense_report_detail.html"

    def get_queryset(self):
        if self.request.user.has_perm("expense_report.manage_expensereport"):
            return ExpenseReport.objects.all()
        return ExpenseReport.objects.filter(created_by=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["log_entries"] = sorted(
            chain(
                *(
                    [self.object.history.all()]
                    + [
                        entry.history.all()
                        for entry in self.object.entries.all()
                    ]
                )
            ),
            key=lambda log_entry: log_entry.timestamp,
            reverse=True,
        )

        last_approved = (
            ExpenseReport.objects.filter(state__in=("approved", "reimbursed"))
            .latest("submitted_at")
        )
        if last_approved in not None:
            last_doc_id = last_approved.document_id
            parts = last_doc_id.split("-")
            context["next_document_id"] = (
                parts[0] + "-" + str(int(parts[1]) + 1).zfill(3)
            )

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.modified_by = self.request.user

        if "generate" in request.POST:
            expense_report_generate_document.delay(self.object.pk)
            self.object.save()
            return HttpResponseRedirect(
                reverse("expense-report-detail", kwargs={"pk": self.object.pk})
            )

        if (
            "submit" in request.POST
            and not self.object.created_by.banking_information.is_complete
        ):
            messages.error(
                self.request,
                "Vos informations bancaires ne sont pas complètes. Mettez-les à jour dans votre profil pour soumettre votre note de frais.",
            )
            return HttpResponseRedirect(
                reverse("expense-report-detail", kwargs={"pk": self.object.pk})
            )

        if (
            "approve" in request.POST
            and not self.object.created_by.banking_information.validated
        ):
            messages.error(
                self.request,
                "Les informations bancaires ne sont pas approuvées. Vérifiez-les dans le profil de l'utilisateur pour pouvoir approuver cette note de frais.",
            )
            return HttpResponseRedirect(
                reverse("expense-report-detail", kwargs={"pk": self.object.pk})
            )

        for transition in self.object.get_available_transitions(request.user):
            if transition not in request.POST:
                continue

            tkwargs = {}
            if transition == "reject":
                if not request.POST.get("reason"):
                    messages.error(
                        self.request, "Veuillez spécifier une raison de rejet."
                    )
                    return HttpResponseRedirect(
                        reverse(
                            "expense-report-detail",
                            kwargs={"pk": self.object.pk},
                        )
                    )
                tkwargs = {
                    "reason": request.POST.get("reason"),
                }
            elif transition == "approve":
                if not request.POST.get("document_id"):
                    messages.error(
                        self.request,
                        "Veuillez spécifier un identifiant de note de frais.",
                    )
                    return HttpResponseRedirect(
                        reverse(
                            "expense-report-detail",
                            kwargs={"pk": self.object.pk},
                        )
                    )
                tkwargs = {
                    "document_id": request.POST.get("document_id"),
                }

            getattr(self.object, transition)(**tkwargs)

            if transition == "destroy":
                return HttpResponseRedirect(reverse("index"))

            self.object.save()
            return HttpResponseRedirect(
                reverse("expense-report-detail", kwargs={"pk": self.object.pk})
            )

        messages.error(self.request, "Quelque chose a mal tourné.")
        return HttpResponseRedirect(reverse("index"))

    def put(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class UserBankingInformationListView(
    PermissionRequiredMixin, LoginRequiredMixin, ListView
):
    template_name = "user_banking_information_list.html"
    model = UserBankingInformation
    permission_required = ("expense_report.manage_expensereport",)

    @method_decorator(transaction.non_atomic_requests)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        if "all" not in self.request.GET:
            qs = qs.filter(validated=False)
        return qs


class UserBankingInformationUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "user_banking_information_update.html"

    def get_queryset(self):
        if self.request.user.has_perm("expense_report.manage_expensereport"):
            return UserBankingInformation.objects.all()
        return UserBankingInformation.objects.filter(user=self.request.user)

    def get_form_class(self):
        if self.request.user.has_perm("expense_report.manage_expensereport"):
            return UserBankingInformationWithValidationForm
        return UserBankingInformationForm

    def get_success_url(self):
        return reverse(
            "user-banking-information-detail", kwargs={"pk": self.object.pk}
        )


class UserBankingInformationDetailView(LoginRequiredMixin, DetailView):
    template_name = "user_banking_information_detail.html"

    def get_queryset(self):
        if self.request.user.has_perm("expense_report.manage_expensereport"):
            return UserBankingInformation.objects.all()
        return UserBankingInformation.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["log_entries"] = self.object.history.all().order_by(
            "-timestamp"
        )

        return context
