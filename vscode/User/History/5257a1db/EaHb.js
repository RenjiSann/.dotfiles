/*
 When pressing Escape, collapse all the accordions
 */
document.addEventListener('keydown', (event) => {
    let accordion_bodies = document.querySelectorAll('.accordion-collapse.collapse');
    if (event.key === 'Escape') {
        accordion_bodies.forEach((acc) => {
            bootstrap.Collapse.getInstance(acc).hide();
        })
    }
});