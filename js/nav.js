/* Functions to facilitate use of nav bar at top of Cope Evans pages */

function displayDropdown(parentDiv) {
    /* This function and dropdown styling adapted from https://www.w3schools.com/howto/howto_js_dropdown.asp */
    document.getElementById(parentDiv).children[1].classList.toggle("show");
}

function showNav() {
    let nav = document.getElementById("nav_list")
    if (nav.style.display == 'block') {
        nav.style.display = 'none'
    }
    else {
        nav.style.display = 'block'
    }
}

window.onclick = function(event) {
    if (!event.target.matches('.essay_button')) {
        var dropdowns = document.getElementsByClassName('essay_options');
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
    if (!event.target.matches('.viz_button')) {
        var dropdowns = document.getElementsByClassName('viz_options');
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}