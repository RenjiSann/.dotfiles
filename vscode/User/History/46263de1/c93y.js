import { INVALID_CLASS, MultiTabForm, formDisplayNthTab, validateForm } from "./form.js"

/// Take the modal id in argument
/// Add an event listener to the modal to reset the form upon opening.
function setupApplicationFormModal(modal_id) {

    const application_form_modal = document.getElementById(modal_id);

    // If the user is not authenticated, form will be null.
    // We will have nothing to do
    const form = application_form_modal.querySelector("form");
    if (form === null) {
        return;
    }

    let multitabform = new MultiTabForm(form);

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
            multitabform.reset();
        }
        event_it_input.setAttribute("value", event_id);
    });
}

setupApplicationFormModal("application-form-modal");
