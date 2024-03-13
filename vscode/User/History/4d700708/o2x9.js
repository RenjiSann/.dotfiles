'use strict';

const STATUS_LIST = {
    "rejected": {
        desc: "Candidature rejetée",
        color: "text-bg-danger",
        label: "rejetée",
    },
    "withdrawn": {
        desc: "Candidature annulée par la candidate",
        color: "text-bg-secondary",
        label: "retirée",
    },
    "cancelled": {
        desc: "Candidature annulée par les organisateurs",
        color: "text-bg-secondary",
        label: "annulée",
    },
    "pending": {
        desc: "Candidature en attente",
        color: "text-bg-warning",
        label: "en attente"
    },
    "accepted": {
        desc: "Candidature acceptée",
        color: "text-bg-info",
        label: "acceptée"
    },
    "confirmed": {
        desc: "Candidature confirmée",
        color: "text-bg-success",
        label: "confirmée"
    },
    "ended": {
        desc: "Stage terminé",
        color: "text-bg-secondary",
        label: "stage terminé"
    }
};

function statusBadge(status) {
    var elm = document.createElement("span");
    elm.classList.add("badge", "rounded-pill", STATUS_LIST[status].color);
    elm.textContent = STATUS_LIST[status].label;
    return elm;
}

function fetchJSON(url) {
    return fetch(url)
        .then(function (response) {
            return response.json();
        });
}

function requestTransition(id, transition) {
    const url = `/rest/applications/${id}/transition/${transition}`;
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(url, {
        method: "POST",
        headers: { "X-CSRFToken": csrftoken }
    });
}

function createTransitionButton(application_id, transition) {
    var button = document.createElement("button");
    button.textContent = transition;
    button.classList.add("btn", "btn-primary");
    button.setAttribute("data-gcc-transition", transition);
    button.addEventListener("click", function (btn) {
        requestTransition(id, transition);
    });
    return button;
}

function updateGCCStatus(gcc_status_element) {
    const id = element.getAttribute("data-gcc-id");
    const st_url = `/rest/applications/${id}/status`;
    const tr_url = `/rest/applications/${id}/transitions`;
}

function main() {

    document.querySelectorAll(".gcc-status-card").forEach(
        function (element) {
            const id = element.getAttribute("data-gcc-id");

            const st_url = `/rest/applications/${id}/status`;
            const tr_url = `/rest/applications/${id}/transitions`;

            // Show current status and transition buttons
            fetchJSON(st_url)
                .then(function (json) {
                    const status = json["status"];

                    element.querySelector(".card-title").appendChild(statusBadge(status));

                    const transitions = json["available_transitions"];
                    transitions.forEach(tr => {
                        const button = createTransitionButton(id, tr)
                        element.appendChild(button);
                    })
                })
        }
    );

}

// If we're already past the "DOM is ready" point, execute immediately:
if (document.readyState === "interactive" || document.readyState === "complete") {
    main();
}
// Otherwise, wait for DOMContentLoaded to fire:
document.addEventListener("DOMContentLoaded", main, { once: true });
