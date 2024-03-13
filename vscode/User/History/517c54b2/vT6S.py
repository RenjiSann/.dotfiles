from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from django_fsm import FSMField, transition

APPLICATION_STATUS = {
    "REJECTED": -3,
    "WITHDRAWN": -2,
    "CANCELLED": -1,
    "PENDING": 0,
    "ACCEPTED": 1,
    "CONFIRMED": 2,
    "ENDED": 3,
}


class SelectionStatus(models.IntegerChoices):
    REJECTED = APPLICATION_STATUS["REJECTED"], _("Candidature rejetée")
    WITHDRAWN = APPLICATION_STATUS["WITHDRAWN"], _(
        "Candidature annulée de la part de la candidate"
    )
    CANCELLED = APPLICATION_STATUS["CANCELLED"], _(
        "Candidature annulée de la part des organisateurs"
    )
    PENDING = APPLICATION_STATUS["PENDING"], _(
        "Candidature en cours de traitement"
    )
    ACCEPTED = APPLICATION_STATUS["ACCEPTED"], _("Candidature acceptée")
    CONFIRMED = APPLICATION_STATUS["CONFIRMED"], _("Candidature confirmée")
    ENDED = APPLICATION_STATUS["ENDED"], _("Stage terminé")


class ApplicationManager(models.Manager):
    def get_applicants(self, event):
        return self.filter(event=event)


class Application(models.Model):
    class Meta:
        verbose_name = _("candidatures")
        verbose_name_plural = _("candidatures")

    event = models.ForeignKey(
        to="events.Event",
        verbose_name=_("Évènement"),
        on_delete=models.CASCADE,
        related_name="applications",
    )

    user = models.ForeignKey(
        to=get_user_model(),
        verbose_name=_("Utilisateur"),
        on_delete=models.CASCADE,
        related_name="applications",
    )

    first_name = models.CharField(
        max_length=256,
        verbose_name=_("Prénom de la participante"),
    )

    last_name = models.CharField(
        max_length=256,
        verbose_name=_("Nom de la participante"),
    )

    dob = models.DateField(
        verbose_name=_("Date de naissance de la participante"),
    )

    email = models.EmailField(
        verbose_name=_("Adresse email de la participante")
    )

    phone = models.CharField(
        max_length=16,
        blank=True,
        verbose_name=_("Numéro de téléphone de la participante"),
    )

    address = models.JSONField(
        verbose_name=_("Adresse de la participante"), default=dict
    )

    first_name_resp = models.CharField(
        max_length=256,
        verbose_name=_("Prénom du responsable légal"),
    )

    last_name_resp = models.CharField(
        max_length=256,
        verbose_name=_("Nom du responsable légal"),
    )

    email_resp = models.EmailField(
        verbose_name=_("Adresse email du responable légal")
    )

    phone_resp = models.CharField(
        max_length=16,
        blank=True,
        verbose_name=_("Numéro de téléphone du responsable légal"),
    )

    address_resp = models.JSONField(
        verbose_name=_("Adresse du responsable légal"), default=dict
    )

    school = models.JSONField(
        verbose_name=_("Etablissement scolaire de la participante"),
        default=dict,
    )

    form_answer = models.JSONField(
        verbose_name=_("Réponse de formulaire"), default=dict
    )

    nb_participations = models.CharField(
        default="",
        verbose_name=_("Nombre de participations de la participante"),
    )

    notes = models.TextField(verbose_name=_("Notes sur la candidatures"))

    # status = models.SmallIntegerField(
    #     choices=SelectionStatus.choices,
    #     verbose_name=_("Statut de la candidature"),
    #     default=0,
    # )
    status = FSMField(
        default=SelectionStatus.PENDING,
        choices=SelectionStatus.choices,
        verbose_name=_("Statut de la candidature"),
        protected=True,
    )

    created_at = models.DateTimeField(
        verbose_name=_("Date d'inscription"),
        auto_now_add=True,
    )

    objects = ApplicationManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}@{self.event}"

    @transition(
        field=status,
        source=SelectionStatus.PENDING,
        target=SelectionStatus.ACCEPTED,
        permission=""
        )
    def accept(self):
        """
        A staff member accept an application
        """
        pass

    @transition(
        field=status,
        source=SelectionStatus.ACCEPTED,
        target=SelectionStatus.CONFIRMED,
        )
    def confirm(self):
        """
        A user confirms its presence to an event
        """
        pass


class ApplicationLabel(models.Model):
    title = models.CharField(max_length=120, verbose_name=_("Titre"))

    class Meta:
        verbose_name = _("label participant")
        verbose_name_plural = _("labels participant")
        ordering = ("title",)

    def __str__(self):
        return self.title
