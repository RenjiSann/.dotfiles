// Must be the same as events/forms.py:PHONE_REGEX
const PHONE_REGEX = /^(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}$/;

const EMAIL_REGEX = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

const INVALID_CLASS = "is-invalid";
const TAB_ACTIVE_CLASS = "active";

class MultiTabForm {
    form;
    next_buttons;
    back_buttons;
    tabs;
    tab_index = 0;
    last_tab_index;

    constructor(form) {
        this.form = form;
        this.next_buttons = form.querySelectorAll("#button-id-next");
        this.back_buttons = form.querySelectorAll("#button-id-back");

        this.tabs = form.querySelectorAll(".tab");
        this.last_tab_index = this.tabs.length - 1;

        // Set event listeners
        this.next_buttons.forEach((btn) => {
            btn.addEventListener("click",
                () => {
                    console.log("YEEET");
                    console.log(this);
                    return this.gotoNextTab();
                }
            )
        });
        this.back_buttons.forEach((btn) => {
            btn.addEventListener("click",
                () => {
                    return this.gotoPrevTab();
                }
            )
        });
        this.form.addEventListener("keydown",
            (event) => {
                if (event.key !== "Enter") {
                    return false;
                }
                if (this.tab_index === this.last_tab_index) {
                    // Do not do anything and let the submit button handler submit
                    return false;
                } else {
                    return this.gotoNextTab();
                }
            }
        );

        // Make sure the first tab is showed
        this.setActiveTab();
    }

    reset() {
        this.form.querySelectorAll("input")
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
        this.form.querySelectorAll("select")
            .forEach((select) => {
                // Remove the red warning if present.
                select.classList.remove(INVALID_CLASS);
                select.selectedIndex = 0;
            });
    }

    validateCurrentTab() {
        let valid = true;
        let fields = this.tabs[this.tab_index].querySelectorAll("input, select");

        fields.forEach((field) => {
            field.classList.remove(INVALID_CLASS);

            if (field.hasAttribute("required")) {
                if (field.type === "checkbox" || field.type === "radio") {
                    if (!field.checked) {
                        valid = false;
                        field.classList.add(INVALID_CLASS);
                    }
                } else if (field.tagName === "select") {
                    // Handle select elements (dropdowns)
                    if (field.value === "") {
                        valid = false;
                        field.classList.add(INVALID_CLASS);
                    }
                } else if (field.value.length == 0) {
                    valid = false;
                    field.classList.add(INVALID_CLASS);
                } else if (field.type === "tel") {
                    // Handle phone validation
                    if (!PHONE_REGEX.test(field.value)) {
                        valid = false;
                        field.classList.add(INVALID_CLASS);
                    }
                } else if (field.type === "email") {
                    if (!EMAIL_REGEX.test(field.value)) {
                        valid = false;
                        field.classList.add(INVALID_CLASS);
                    }
                }
            }
        });
        return valid;
    }

    setActiveTab() {
        this.tabs
            .forEach((tab, index) => {
                if (index === this.tab_index) {
                    tab.classList.add(TAB_ACTIVE_CLASS);
                } else {
                    tab.classList.remove(TAB_ACTIVE_CLASS);
                }
            });
    }

    gotoNextTab() {
        if (this.tab_index === this.last_tab_index) {
            return false;
        }
        if (!this.validateCurrentTab()) {
            return false;
        }
        this.tab_index++;
        this.setActiveTab();
    }

    gotoPrevTab() {
        if (this.tab_index === 0) {
            return false;
        }
        this.tab_index--;
        this.setActiveTab();
    }
}

export {
    MultiTabForm,
};
