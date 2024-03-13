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
    elm.classList.add("badge", "rounded-pill", "gcc-status-badge", STATUS_LIST[status].color);
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
        headers: { "X-CSRFToken": csrftoken },
    }).then(
        function (data) {
            // Update was successful, update page
            const query = `.gcc-status-card[data-gcc-id="${id}"]`;
            var element = document.querySelector(query);
            updateGCCStatus(element);
        }
    );
}

function createTransitionButton(application_id, transition) {
    var button = document.createElement("button");
    button.textContent = transition;
    button.classList.add("btn", "btn-primary");
    button.setAttribute("data-gcc-transition", transition);
    button.addEventListener("click", function (_) {
        requestTransition(application_id, transition);
    });
    return button;
}

function updateGCCStatus(gcc_status_element) {
    console.log(gcc_status_element);
    const id = gcc_status_element.getAttribute("data-gcc-id");
    const url = `/rest/applications/${id}/status`;

    // Show current status and transition buttons
    fetchJSON(url)
        .then(function (json) {
            const status = json["status"];

            gcc_status_element
                .querySelector(".card-title > .gcc-status-badge")
                .replaceWith(statusBadge(status));
            // Replace row badge
            document
                .querySelector(`td[data-gcc-id="${id}"] .gcc-status-badge`)
                .replaceWith(statusBadge(status));

            let card_body = gcc_status_element.querySelector(".card-text");
            card_body.innerHTML = ''; // Clear inside

            const transitions = json["available_transitions"];
            transitions.forEach(tr => {
                const button = createTransitionButton(id, tr)
                card_body.appendChild(button);
            })
        })
}

function main() {

    document.querySelectorAll(".gcc-status-card").forEach(
        function (element) {
            updateGCCStatus(element);
        }
    );

    document.querySelectorAll(".gcc-notes-card").forEach(
        function(element) {

        }
    )

}

// If we're already past the "DOM is ready" point, execute immediately:
if (document.readyState === "interactive" || document.readyState === "complete") {
    main();
}
// Otherwise, wait for DOMContentLoaded to fire:
document.addEventListener("DOMContentLoaded", main, { once: true });
