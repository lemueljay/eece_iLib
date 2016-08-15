/*

CUSTOM JAVASCRIPT

*/


jQuery(document).ready(function ($) {

    $('#btn-nav-mobile').on('click', function () {
        $('#site-nav-mobile').slideToggle(function() {
            $('#site-nav-mobile > ul').css('show-mobile');
        });
    });

});