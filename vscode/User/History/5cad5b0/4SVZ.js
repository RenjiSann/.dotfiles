import { MultiTabForm, formDisplayNthTab, validateForm } from "./form.js"

/// Take the form HTML element as argument
function setupRegistrationForm(form)  {
    let multitabform = new MultiTabForm(form);
}

setupRegistrationForm(document.querySelector("form"));
