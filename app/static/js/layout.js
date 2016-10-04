// These are the scripts that required for some layout to function in the application

$(document).ready(function() {
    // Initialize collapse button
    $(".button-collapse").sideNav('show');
    $(".button-collapse").sideNav('show');
    $('.button-collapse').sideNav({
        menuWidth: 300,
        edge: 'left',
        closeOnClick: false
    });
    $('.collapsible').collapsible();

    $('select').material_select();
    $('.modal-trigger').leanModal()
    $(".dropdown-button").dropdown();
})