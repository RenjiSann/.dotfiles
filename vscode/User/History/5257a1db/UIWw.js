/*
 When pressing Escape, collapse all the accordions
 */
let accordion_bodies = document.querySelectorAll('.accordion-collapse.collapse');
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        accordion_bodies.forEach((acc) => {
            let collapse = bootstrap.Collapse.getInstance(acc);
            console.log(acc);
            console.log(collapse);
            collapse.hide();
        })
    }
});