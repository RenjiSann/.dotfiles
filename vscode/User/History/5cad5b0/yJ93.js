import { MultiTabForm, formDisplayNthTab, validateForm } from "./form.js"

/// Take the form HTML element as argument
function setupRegistrationForm(form)  {
    // Add event listeners for prev/next buttons
    const next_buttons = form.querySelectorAll("#button-id-next");
    const back_buttons = form.querySelectorAll("#button-id-back");
    let tab_index = 0;

    next_buttons.forEach(function (btn) {
        btn.addEventListener("click",
            function () {
                // Do not go to next page if there is invalid data
                if (!validateForm(form)) {
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
    formDisplayNthTab(form, tab_index);
}

setupRegistrationForm(document.querySelector("form"));
