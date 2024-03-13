import { PHONE_REGEX, INVALID_CLASS, TAB_ACTIVE_CLASS } from "./form.js"

/// Take a form HTML element and a positive integer as arguments.
/// Add display: none to all the disabled tabs.
function formDisplayNthTab(form, n) {
    form.querySelectorAll(".tab")
        .forEach((tab, index) => {
            if (index === n) {
                tab.classList.add(TAB_ACTIVE_CLASS);
            } else {
                tab.classList.remove(TAB_ACTIVE_CLASS);
            }
        });
}

/// Take the form HTML element in argument.
/// - Removes all user added data and reset all placeholders to defaults
/// - Set the view to the 1st tab.
function clearApplicationForm(form) {
    // Select all user inputs
    form.querySelectorAll("input")
        .forEach(input => {
            const type = input.getAttribute("type");

            // If not a user-editable input, return
            if (type === "hidden"     // CRSF token etc...
                || type === "button"  // prev/next/submit btns
            ) {
                return;
            }

            // Remove the red warning if present
            input.classList.remove(INVALID_CLASS);
            // Reset the value to the default
            if (type === "checkbox") {
                input.checked = false;
            } else {
                input.value = input.getAttribute("value");
            }
        });

    // Reset selectors to default choice
    form.querySelectorAll("select")
        .forEach(select => {
            // Remove the red warning if present.
            select.classList.remove(INVALID_CLASS);
            select.selectedIndex = 0;
        });

    // Reset application form tab.
    formDisplayNthTab(form, 0);
}

/// Take the form HTML element as argument.
/// @return true if the current form tab is correctly filled.
function validateApplicationForm(form) {
    let valid = true;
    let active_tab = form.querySelector(".tab.active");
    let fields = active_tab.querySelectorAll("input, select");
    fields.forEach(function (val) {
        val.classList.remove(INVALID_CLS);

        if (val.hasAttribute("required")) {
            if (val.type === "checkbox" || val.type === "radio") {
                if (!val.checked) {
                    valid = false;
                    val.classList.add(INVALID_CLS);
                }
            } else if (val.tagName === "select") {
                // Handle select elements (dropdowns)
                if (val.value === "") {
                    valid = false;
                    val.classList.add(INVALID_CLS);
                }
            } else if (val.value.length == 0) {
                valid = false;
                val.classList.add(INVALID_CLS);
            } else if (val.type === "tel") {
                // Handle phone validation
                if (!PHONE_REGEX.test(val.value)) {
                    valid = false;
                    val.classList.add(INVALID_CLS);
                }
            }
        }
    });
    return validate;
}

/// Take the modal id in argument
/// Add an event listener to the modal to reset the form upon opening.
function setupApplicationFormModal(modal_id) {

    const application_form_modal = document.getElementById(modal_id);

    // If the user is not authenticated, form will be null.
    // We will have nothing to do
    const form = application_form_modal.querySelector("form");
    if (form == null) {
        return;
    }

    // Add event effects on modal opening.
    // - Update event_id
    // - Clear form, go to 1st tab
    application_form_modal.addEventListener("show.bs.modal", js_event => {

        // When the modal appears, find the id of the event related
        // to the button that was pressed.
        const button = js_event.relatedTarget;
        const event_id = button.getAttribute("data-bs-event-id");
        console.log("Opening application modal for event ID #" + event_id);

        // Update the form's event id, and reset its content.
        // Check current form id. if new event ID, reset its content.
        let event_it_input = form.querySelector("#event-id-input");
        const previous_id = event_it_input.getAttribute("value");

        if (previous_id != null && previous_id != event_id) {
            clearApplicationForm(form);
        }
        event_it_input.setAttribute("value", event_id);
    });

    // Add event listeners for prev/next buttons
    const next_buttons = form.querySelectorAll("#button-id-next");
    const back_buttons = form.querySelectorAll("#button-id-back");
    let tab_index = 0;

    next_buttons.forEach(function (btn) {
        btn.addEventListener("click",
            function () {
                // Do not go to next page if there is invalid data
                if (!validateApplicationForm(form)) {
                    return false;
                }
                formDisplayNthTab(form, ++tab_index);
            })
    });
    back_buttons.forEach(function (btn) {
        btn.addEventListener("click",
            function () {
                formDisplayNthTab(form, --tab_index);
            })
    });

    // Ensure the first tab is opened at page loading
    formDisplayNthTab(tab_index);
}

setupApplicationFormModal("application-form-modal");
