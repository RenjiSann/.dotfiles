
@admin.register(models.Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "first_name",
        "last_name",
        "status",
        "event",
    )

    raw_id_fields = (
        "user",
        "event",
    )

    search_fields = (
        "first_name",
        "last_name",
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
    )

    list_filter = (
        "status",
        "event",
    )

    fieldsets = (
        (None, {"fields": ("user", "event")}),
        (
            "Informations participante",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "phone",
                    "dob",
                    "form_answer",
                    "address",
                )
            },
        ),
        (
            "Responsable légal",
            {"fields": ("email_resp", "phone_resp", "address_resp")},
        ),
        (
            "Sélection",
            {
                "fields": (
                    "nb_participations",
                    "status",
                    "notes",
                ),
            },
        ),
    )


@admin.register(models.ApplicationLabel)
class ApplicationLabelAdmin(admin.ModelAdmin):
    search_fields = ("title",)