_BASE_CTX = {
    "ADDRESS_LINE_1": "Association Prologin",
    "ADDRESS_LINE_2": "14-16 rue Voltaire",
    "ADDRESS_LINE_3": "94270 Le Kremlin-Bicêtre",
    "CONTACT_EMAIL": "info@girlscancode.fr",
    "CONTACT_PHONE": "+33 (0)1 44 08 01 90",
    "SCHOLARSHIP_EMAIL": "bourse@girlscancode.fr",
    "PARTNERS_EMAIL": "partenaires@girlscancode.fr",
    "CNIL_DECL_NUM": "830039",
}


def my_context_processor(req):
    context = _BASE_CTX
    social_networks = [
        {
            "link": "https://www.instagram.com/association_prologin/",
            "logo": "fa-instagram",
            "alt": "Page Instagram de l'association Prologin",
        },
        {
            "link": "https://www.flickr.com/photos/prologin/",
            "logo": "fa-flickr",
            "alt": "Album photos de l'association Prologin",
        },
        {
            "link": "https://fr.linkedin.com/company/prologin",
            "logo": "fa-linkedin",
            "alt": "Page LinkedIn de l'association Prologin",
        },
        {
            "link": "https://www.facebook.com/stagegirlscancode/",
            "logo": "fa-facebook",
            "alt": "Page Facebook des stages Girls Can Code!",
        },
        {
            "link": "https://twitter.com/prologin",
            "logo": "fa-twitter",
            "alt": "Page Twitter de l'association Prologin",
        },
    ]
    faq_entries = [
        {
            "question": "Qu'est-ce qu'un stage GCC! ?",
            "answer": """
            <p>
                Pendant un stage Girls Can Code!, vous aurez l'occasion
                d'apprendre et de pratiquer la programmation tout en étant
                accompagnée par des étudiantes et des étudiants en
                informatique. Ce sera l'occasion pour vous de découvrir le
                domaine du numérique et vous aider dans votre orientation.
            </p>

            <p>
                Deux types de stages sont proposés, les stages courts qui
                se déroulent le temps d'un week-end et les stages longs
                qui durent une semaine.
            </p>

            <p>
                Des femmes venant du monde du numérique interviennent lors
                des stages sur leur parcours scolaire et professionnel.
            </p>
            """,
        },
        {
            "question": "Qui peux s'inscrire aux stages ?",
            "answer": """
            Toute personne s'identifiant comme une femme et étant actuellement
            ou à la rentrée prochaine dans l'enseignement secondaire (collège
            et lycée) ou équivalent peut s'inscire aux stages Girls Can Code!.
            """,
        },
        {
            "question": "Combien coûte un stage ?",
            "answer": f"""Nous prenons en charge l'ensemble des repas ainsi que tous les frais relatifs aux activités pendant le stage. Si vous avez besoin d'une aide financière pour le logement et/ou le transport vous pouvez faire une demande de bourse à <a href="mailto:f{context['SCHOLARSHIP_EMAIL']}">{context['SCHOLARSHIP_EMAIL']}</a>. Nous pouvons aussi vous mettre en relation avec les autres familles volontaires pour l'hébergement ou pour du covoiturage, pour cela envoyez un mail à <a href="mailto:{context['CONTACT_EMAIL']}">{context['CONTACT_EMAIL']}</a>.""",
        },
        {
            "question": "Quels sont les critères de sélection ?",
            "answer": "Nous nous basons principalement sur la motivation et réponses lors de la candidature. Le niveau n'est absolument pas un critère car nous adaptons les exercices en fonction de celui-ci. Les filles n'ayant jamais participé à nos stages sont prioritaires par rapport à celles qui en ont déjà fait.",
        },
        {
            "question": "Quel est le niveau requis pour participer ?",
            "answer": "Il n'y a pas de niveau minimal. Nous nous adaptons à tous les niveaux, il ne faut pas hésiter à nous informer d'éventuels sujets spécifiques que vous souhaitez découvrir ou approfondir. Nous nous adaptons à tous les profils.",
        },
        {
            "question": "Qui organise le stage ?",
            "answer": "Nous sommes l'association Prologin et en plus des stages \"Girls Can Code!\", nous organisons le concours <a href=\"https://prologin.org\">Prologin</a>. Notre but est de promouvoir l'informatique auprès des jeunes. Les encadrants sont principalement des étudiants et étudiantes en informatique. Ils sont là pour vous aider dans les exercices et répondre à toutes vos questions que ce soit d'informatique ou d'orientation.",
        },
        {
            "question": "Comment bénéficier de la bourse ?",
            "answer": f"""Il suffit d'envoyer un mail à <a href="mailto:{context['SCHOLARSHIP_EMAIL']}">{context['SCHOLARSHIP_EMAIL']}</a>. et l'ensemble de la procédure vous sera transmise par un responsable de l'association.""",
        },
        {
            "question": "Peut-on faire le stage plusieurs fois ?",
            "answer": "Oui, c'est possible. Cependant, gardez à l'esprit que vous ne serez pas prioritaire lors de la sélection. De plus, il est possible que vous ayez déjà exploré toutes les notions que nous proposons.",
        },
        {
            "question": "Je ne suis pas éligible aux stages GCC!, que me suggérez-vous ?",
            "answer": '<h3>Si tu as déjà codé</h3><p>Nous te proposons de participer au concours <a href="https://prologin.org">Prologin</a>.<h3>Si tu souhaites débuter</h3> Tu peux te laisser guider par les exercices de <a href="http://www.france-ioi.org/">France-IOI</a> et si tu te débrouilles en anglais, il y a <a href="https://www.codecademy.com/">Codecademy</a>.</p>',
        },
    ]

    button_sns = [
        {
            "logo": "google",
            "name": "Google",
        },
        {
            "logo": "twitter",
            "name": "Twitter",
        },
        {
            "logo": "instagram",
            "name": "Instagram",
        },
        {
            "logo": "facebook",
            "name": "Facebook",
        },
    ]

    context["SOCIAL_NETWORKS"] = social_networks  # type: ignore
    context["FAQ_ENTRIES"] = faq_entries  # type: ignore
    context["BUTTON_SNS"] = button_sns  # type: ignore

    return context


# -------------------------------#
#        PRIVACY CONTEXTS        #
# -------------------------------#

# Le premier élément de la liste à puce est le même pour
# toutes les pages
_PRIVACY_BASE_CTX = {
    "title": "Vos droits sur vos données",
    "content": f"""
    <h4>L'essentiel</h4>
    <p>
        Vous disposez (le cas échéant <em>via</em> le responsable légal) des droits
        d'accéder et d'obtenir copie des données vous concernant,
        de vous opposer au traitement de ces données,
        de les faire rectifier ou les faire effacer.
        Vous disposez également d'un droit à la limitation du traitement de vos données.
        Vous pouvez retirer à tout moment votre consentement au traitement de vos données.
        Vous pouvez également exercer votre droit à la portabilité de vos données.
        <a href="https://www.cnil.fr/fr/comprendre-vos-droits">
            Rendez-vous sur le site de la CNIL pour mieux comprendre vos droits
        </a>.
    </p>
    <h4>Exercer vos droits</h4>
    <p>
        Toute demande d'exercice de vos droits doit être adressée par voie électronique à
        <a href="mailto:{_BASE_CTX['CONTACT_EMAIL']}">
            {_BASE_CTX['CONTACT_EMAIL']}
        </a>.
    </p>
    <h4>Réclamation auprès de la CNIL</h4>
    <p>
        Si vous estimez, après nous avoir contacté, que vos droits sur vos données ne sont pas respectés,
        vous pouvez alors
        <a href="https://www.cnil.fr/fr/webform/adresser-une-plainte">
            adresser une réclamation à la CNIL
        </a>.
    </p>
    """,
}


def privacy_inscription_list():
    return [
        {
            "title": "Objet du traitement de données",
            "content": """
            <h4>Finalités</h4>
            <p>Le traitement a pour objet <strong>l’inscription sur le site Girls Can Code! (GCC!)</strong>.</p>
            <h4>Base légale</h4>
            <p>Ce traitement repose sur le consentement des inscrits et de leur responsable légal le cas échéant (mineurs de 15 ans), ce sont les articles 6(1)a et 8 du RGPD, et 45 de la Loi Informatique et Libertés.</p>
            """,
        },
        {
            "title": "Personnes concernées",
            "content": "<p>Le traitement de données concerne les personnes physiques souhaitant s’inscrire au site GCC!.</p>",
        },
        {
            "title": "Données traitées",
            "content": """
            <h4>Catégories de données traitées</h4>
            <ul>
                <li>Données d'identification : nom, prénom, adresse email ;</li>
                <li>Internet : mesure d'audience.</li>
            </ul>
            <h4>Source des données</h4>
            <p>Ces informations sont recueillies directement auprès de la participante, et/ou de son responsable légal le cas échéant (mineurs de 15 ans).</p>
            <h4>Caractère obligatoire des réponses</h4>
            <p>L'inscription au site GCC! prévoit, sauf mention contraire, le recueil obligatoire de données qui sont nécessaires au traitement de l'inscription.</p>
            <h4>Prise de décision automatisée</h4>
            <p>Le traitement ne prévoit pas de prise de décision automatisée.</p>
            """,
        },
        {
            "title": "Destinataires des données",
            "content": """
            <h4>Catégories de destinataires</h4>
            <p>En fonction de leurs besoins respectifs, sont destinataires de tout ou partie des données : </p>
            <ul>
                <li>les membres autorisés de Prologin ;</li>
                <li>les membres autorisés des sous-traitants de Prologin ;</li>
            </ul>
            <h4>Transfert des données hors UE</h4>
            <p>Aucun transfert de données hors de l'Union européenne n'est réalisé.</p>
            """,
        },
        {
            "title": "Durée de conservation",
            "content": """
            <p>Les nom et prénom de la personne sont conservés en base active jusqu'à sa désinscription.
            L'adresse email est gardée dans les sauvegardes 6 mois supplémentaires après la désinscription.</p>
            """,
        },
        {
            "title": "Sécurité",
            "content": "<p>Des mesures de sécurité visant à garantir la confidentialité, l'intégrité et la disponibilité des données collectées, issues du référentiel ISO/IEC27002 ont été mises en œuvre. Elles comprennent, sans s'y limiter, le chiffrement des données en transit et leur sauvegarde régulière externalisée.</p>",
        },
        _PRIVACY_BASE_CTX,
    ]


def privacy_stage_list():
    return [
        {
            "title": "Objet du traitement de données",
            "content": """
            <h4>Finalités</h4>
            <p>Le traitement a pour objet <strong>l'organisation des stages Girls Can Code! (GCC!)</strong>.<br>Il permet à l'association Prologin :</p>
            <ul>
                <li>de traiter les demandes de participation ;</li>
                <li>d'attribuer ou non une bourse financière ;</li>
                <li>d'adapter le contenu pédagogique aux attentes des participantes ;</li>
                <li>d'adapter les repas aux contraintes alimentaires de chacune ;</li>
                <li>de répondre aux sollicitations de la part des participantes ;</li>
                <li>de piloter les stages (évaluation de la satisfaction des participantes, production de statistiques).</li>
            </ul>
            <h4>Base légale</h4>
            <p>Ce traitement repose sur le consentement des inscrits et de leur responsable légal le cas échéant (mineures de 16 ans), ce sont les articles 6(1)a et 8 du RGPD.</p>
            """,
        },
        {
            "title": "Personnes concernées",
            "content": """
            <p>Le traitement de données concerne :</p>
            <ul>
                <li>les personnes physiques souhaitant participer à un stage GCC! ;</li>
                <li>les responsables légaux des personnes ci-dessus le cas échéant (mineures de 16 ans) ;</li>
            </ul>
            """,
        },
        {
            "title": "Données traitées",
            "content": """
            <h4>Catégories de données traitées</h4>
            <ul>
            <li>Données d'identification : nom, prénom, adresse postale... ;</li>
            <li>Vie scolaire (dite professionnelle) : niveau d'étude ;</li>
            <li>Vie personnelle : habitudes alimentaires ;</li>
            <li>Informations d'ordre économique et financier, si une demande de bourse est faite par la participante ;</li>
            <li>Internet : mesure d'audience ;</li>
            <li>Données de santé : éventuels traitements médicaux et allergies.</li>
        </ul>
        <h4>Source des données</h4>
        <p>Ces informations sont recueillies directement auprès de la participante, et/ou de son responsable légal le cas échéant (mineures de 16 ans).</p>
        <h4>Caractère obligatoire des réponses</h4>
        <p>L'inscription à un stage GCC! prévoit, sauf mention contraire, le recueil obligatoire de données qui sont nécessaires au traitement de l'inscription.</p>
        <h4>Prise de décision automatisée</h4>
        <p>Le traitement ne prévoit pas de prise de décision automatisée : toutes les demandes d'inscription sont revues par un être humain :)</p>
            """,
        },
        {
            "title": "Destinataires des données",
            "content": """
            <h4>Catégories de destinataires</h4>
            <p>En fonction de leurs besoins respectifs, sont destinataires de tout ou partie des données : </p>
            <ul>
                <li>les membres autorisés de Prologin ;</li>
                <li>les membres autorisés des partenaires et/ou sous-traitants de Prologin ;</li>
                <li>les autres participantes à un même stage ;</li>
                <li>les services de secours d'urgence en cas de besoin.</li>
            </ul>
            <h4>Transfert des données hors UE</h4>
            <p>Aucun transfert de données hors de l'Union européenne n'est réalisé.</p>
            """,
        },
        {
            "title": "Durée de conservation",
            "content": """
            <p>
                Les données d’identification, de vie scolaire et personnelle sont conservées jusqu'à la fin du stage en base active,
                puis 6 mois supplémentaires en sauvegarde.
                <br>Les informations d'ordre économique et financier sont conservées le temps d'attribuer ou non une bourse plus un mois.
                <br>Les données de santé sont conservées jusqu'à 3 ans après la fin du stage.
            </p>
            """,
        },
        {
            "title": "Sécurité",
            "content": "<p>Des mesures de sécurité visant à garantir la confidentialité, l'intégrité et la disponibilité des données collectées, issues du référentiel ISO/IEC27002 ont été mises en œuvre. Elles comprennent, sans s'y limiter, le chiffrement des données en transit et leur sauvegarde régulière externalisée.</p>",
        },
        _PRIVACY_BASE_CTX,
    ]


def privacy_newsletter_list():
    return [
        {
            "title": "Objet du traitement de données",
            "content": """
            <h4>Finalités</h4>
            <p>Le traitement a pour objet <strong>l'inscription à la newsletter Girls Can Code! (GCC!)</strong>.<br>Il permet à l'association Prologin :</p>
            <ul>
                <li>de communiquer autour des stages Girls Can Code!</li>
            </ul>
            <h4>Base légale</h4>
            <p>Ce traitement repose sur le consentement des inscrits et de leur responsable légal le cas échéant (mineures de 16 ans), ce sont les articles 6(1)a et 8 du RGPD.</p>
            """,
        },
        {
            "title": "Personnes concernées",
            "content": """
            <p>Le traitement de données concerne :</p>
            <ul>
                <li>les personnes physiques souhaitant être informées des activités l'association Prologin relatives aux stages GCC! ;</li>
                <li>les responsables légaux des personnes ci-dessus le cas échéant (mineures de 16 ans) ;</li>
            </ul>
            """,
        },
        {
            "title": "Données traitées",
            "content": """
            <h4>Catégories de données traitées</h4>
            <ul>
                <li>Données d'identification : adresse email ;</li>
                <li>Internet : mesure d'audience.</li>
            </ul>
            <h4>Source des données</h4>
            <p>Ces informations sont recueillies directement auprès de la participante, et/ou de son responsable légal le cas échéant (mineures de 16 ans).</p>
            <h4>Caractère obligatoire des réponses</h4>
            <p>L'inscription à la newsletter GCC! prévoit, sauf mention contraire, le recueil obligatoire de données qui sont nécessaires au traitement de l'inscription.</p>
            <h4>Prise de décision automatisée</h4>
            <p>Le traitement ne prévoit pas de prise de décision automatisée.</p>
            """,
        },
        {
            "title": "Destinataires des données",
            "content": """
            <h4>Catégories de destinataires</h4>
            <p>En fonction de leurs besoins respectifs, sont destinataires de tout ou partie des données : </p>
            <ul>
                <li>les membres autorisés de Prologin ;</li>
<li>les sous-traitants autorisés de Prologin pour la gestion de l'inscription et l'envoi de la newsletter.</li>
            </ul>
            <h4>Transfert des données hors UE</h4>
            <p>Aucun transfert de données hors de l'Union européenne n'est réalisé.</p>
            """,
        },
        {
            "title": "Durée de conservation",
            "content": "<p>Les données d’identification sont conservées jusqu'à la désinscription de la personne.</p>",
        },
        {
            "title": "Sécurité",
            "content": "<p>Des mesures de sécurité visant à garantir la confidentialité, l'intégrité et la disponibilité des données collectées, issues du référentiel ISO/IEC27002 ont été mises en œuvre. Elles comprennent, sans s'y limiter, le chiffrement des données en transit et leur sauvegarde régulière externalisée.</p>",
        },
        _PRIVACY_BASE_CTX,
    ]
