from django.db import models
from django.utils.translation import gettext_lazy as _
from django_fsm import FSMField, transition

from profiles.models import Profile


class ApplicationStatus(models.TextChoices):
    REJECTED = "rejected", _("Candidature rejetée")
    WITHDRAWN = "withdrawn", _("Candidature annulée par la candidate")
    CANCELLED = "cancelled", _("Candidature annulée par les organisateurs")
    PENDING = "pending", _("Candidature en cours de traitement")
    ACCEPTED = "accepted", _("Candidature acceptée")
    CONFIRMED = "confirmed", _("Candidature confirmée")
    ENDED = "ended", _("Stage terminé")


class TshirtSize(models.TextChoices):
    __empty__ = "-"
    XS = ("XS", "XS")
    S = ("S", "S")
    M = ("M", "M")
    L = ("L", "L")
    XL = ("XL", "XL")
    XXL = ("XXL", "XXL")


class ApplicationManager(models.Manager):
    def get_applicants(self, event):
        return self.filter(event=event)


class Application(models.Model):
    event = models.ForeignKey(
        to="events.Event",
        verbose_name=_("Évènement"),
        on_delete=models.CASCADE,
        related_name="applications",
    )

    profile = models.ForeignKey(
        to=Profile,
        verbose_name=_("Profil"),
        on_delete=models.SET_NULL,
        related_name="applications",
        null=True,
        blank=True,
    )

    tshirt = models.CharField(
        verbose_name=_("Taille de tshirt"),
        max_length=3,
        choices=TshirtSize.choices,
    )

    form_answer = models.JSONField(
        verbose_name=_("Réponse de formulaire"), default=dict
    )

    notes = models.TextField(
        verbose_name=_("Notes sur la candidatures"), blank=True
    )

    status = FSMField(
        default=ApplicationStatus.PENDING,
        choices=ApplicationStatus.choices,
        verbose_name=_("Statut de la candidature"),
        protected=True,
    )

    created_at = models.DateTimeField(
        verbose_name=_("Date d'inscription"),
        auto_now_add=True,
    )

    objects = ApplicationManager()

    class Meta:
        verbose_name = _("candidatures")
        verbose_name_plural = _("candidatures")
        permissions = [
            ("manage_applications", "Can manage the status of applications"),
            (
                "override_applications",
                "Can override the application status flow",
            ),
        ]
        unique_together = ("event", "profile")

    def __str__(self):
        if self.profile:
            return f"{self.profile}({self.profile.user_id})@{self.event}"
        else:
            return f"-@{self.event}"

    def save(self, *args, **kwargs):
        """
        When saving the model, if profile is none, switch the status to CANCELLED
        """
        if not self.profile:
            self.profile = None
        super().save(*args, **kwargs)

    @property
    def first_name(self):
        if self.profile is None:
            return "<deleted-profile>"
        return self.profile.first_name

    @property
    def last_name(self):
        if self.profile is None:
            return "<deleted-profile>"
        return self.profile.last_name

    @property
    def email(self):
        if self.profile is None:
            return "<deleted-profile>"
        return self.profile.email

    @property
    def phone(self):
        if self.profile is None:
            return "<deleted-profile>"
        return self.profile.phone

    @property
    def birth_date(self):
        if self.profile is None:
            return "<deleted-profile>"
        return self.profile.birth_date

    @property
    def first_name_resp(self):
        if self.profile is None:
            return "<deleted-profile>"
        return self.profile.first_name_resp

    @property
    def last_name_resp(self):
        if self.profile is None:
            return "<deleted-profile>"
        return self.profile.last_name_resp

    @property
    def email_resp(self):
        if self.profile is None:
            return "<deleted-profile>"
        return self.profile.email_resp

    @property
    def phone_resp(self):
        if self.profile is None:
            return "<deleted-profile>"
        return self.profile.phone_resp

    @property
    def school_name(self):
        if self.profile is None:
            return "<deleted-profile>"
        return self.profile.school_name

    @property
    def address(self):
        if self.profile is None:
            return "<deleted-profile>"
        res = f"{self.profile.street_app}"
        if self.profile.complement_app:
            res += f"{self.profile.complement_app}"
        res += f", {self.profile.zipcode_app} {self.profile.city_app}"
        return res

    @property
    def address_resp(self):
        if self.profile is None:
            return "<deleted-profile>"
        res = f"{self.profile.street_resp}"
        if self.profile.complement_resp:
            res += f"{self.profile.complement_resp}"
        res += f", {self.profile.zipcode_resp} {self.profile.city_resp}"
        return res

    @property
    def address_school(self):
        if self.profile is None:
            return "<deleted-profile>"
        res = f"{self.profile.street_school}"
        if self.profile.complement_school:
            res += f"{self.profile.complement_school}"
        res += f", {self.profile.zipcode_school} {self.profile.city_school}"
        return res


    @staticmethod
    def _transition_perm_owner(instance, user):
        return (
            instance.profile
            and instance.profile.user == user
        )

    @staticmethod
    def _transition_perm_owner_or_staff(instance, user):
        return (
            instance.profile
            and instance.profile.user == user
            or user.has_perm("applications.manage_applications")
        )

    @staticmethod
    def _transition_perm_staff(_, user):
        return user.has_perm("applications.manage_applications")

    @staticmethod
    def _transition_perm_override(_, user):
        return user.has_perm("applications.override_applications")

    # -----------
    # TRANSITIONS
    # -----------

    @transition(
        field=status,
        source=ApplicationStatus.PENDING,
        target=ApplicationStatus.ACCEPTED,
        permission=_transition_perm_staff,
    )
    def accept(self):
        """
        A staff member accept an application
        """
        # TODO: Send mail to the girl
        pass

    @transition(
        field=status,
        source=ApplicationStatus.PENDING,
        target=ApplicationStatus.REJECTED,
        permission=_transition_perm_staff,
    )
    def reject(self):
        """
        A staff member rejects an application
        """
        # TODO: Send mail to the girl
        pass

    @transition(
        field=status,
        source=ApplicationStatus.ACCEPTED,
        target=ApplicationStatus.CONFIRMED,
        permission=_transition_perm_user_or_staff,
    )
    def confirm(self):
        """
        A user confirms its presence to an event
        """
        # TODO: Send mail to prologin
        pass

    @transition(
        field=status,
        source=[
            ApplicationStatus.PENDING,
            ApplicationStatus.ACCEPTED,
            ApplicationStatus.CONFIRMED,
        ],
        target=ApplicationStatus.WITHDRAWN,
        permission=_transition_perm_user_or_staff,
    )
    def withdraw(self):
        """
        A user cancels its application
        """
        # TODO: Send a mail to prologin => with WARNING if source status was
        # 'confirmed'

    @transition(
        field=status,
        source=[
            ApplicationStatus.PENDING,
            ApplicationStatus.ACCEPTED,
            ApplicationStatus.CONFIRMED,
        ],
        target=ApplicationStatus.CANCELLED,
        permission=_transition_perm_staff,
    )
    def cancel(self, reason=None):
        """
        An application is cancelled, mostly because the event is cancelled
        """
        # TODO: Send a mail to user => with WARNING if source status was
        # 'confirmed'
        pass

    @transition(
        field=status,
        source=ApplicationStatus.CONFIRMED,
        target=ApplicationStatus.ENDED,
    )
    def set_event_ended(self):
        """
        A confirmed application is ended because the event has passed.
        This transition should be triggered automatically,
        not at someone's request.
        """
        pass

    # -----------------
    # ADMIN TRANSITIONS
    # -----------------

    @transition(
        field=status,
        target=ApplicationStatus.REJECTED,
        permission=_transition_perm_override,
        custom=dict(admin=True),
    )
    def force_rejected(self):
        """
        Admin-resserved transition to rejected
        """
        pass

    @transition(
        field=status,
        target=ApplicationStatus.ENDED,
        permission=_transition_perm_override,
        custom=dict(admin=True),
    )
    def force_ended(self):
        """
        Admin-resserved transition to ended
        """
        pass

    @transition(
        field=status,
        target=ApplicationStatus.CANCELLED,
        permission=_transition_perm_override,
        custom=dict(admin=True),
    )
    def force_cancelled(self):
        """
        Admin-resserved transition to cancelled
        """
        pass

    @transition(
        field=status,
        target=ApplicationStatus.PENDING,
        permission=_transition_perm_override,
        custom=dict(admin=True),
    )
    def force_pending(self):
        """
        Admin-resserved transition to pending
        """
        pass

    @transition(
        field=status,
        target=ApplicationStatus.ACCEPTED,
        permission=_transition_perm_override,
        custom=dict(admin=True),
    )
    def force_accepted(self):
        """
        Admin-resserved transition to accepted
        """
        pass

    @transition(
        field=status,
        target=ApplicationStatus.CONFIRMED,
        permission=_transition_perm_override,
        custom=dict(admin=True),
    )
    def force_confirmed(self):
        """
        Admin-resserved transition to accepted
        """
        pass

    def get_available_transitions_names(self, user=None, remove_forced=True):
        """
        Return a list of currently possible transitions with the current user
        """
        transitions = []
        if not user:
            transitions = self.get_available_status_transitions()
        else:
            transitions = self.get_available_user_status_transitions(user)

        transition_names = [
            t.name
            for t in transitions
            if not remove_forced or not t.name.startswith("force_")
        ]
        return transition_names


class ApplicationLabel(models.Model):
    title = models.CharField(max_length=120, verbose_name=_("Titre"))

    class Meta:
        verbose_name = _("label participant")
        verbose_name_plural = _("labels participant")
        ordering = ("title",)

    def __str__(self):
        return self.title
