/*

CUSTOM JAVASCRIPT

*/


// function scrollFixed() {
//     var window_top = $(window).scrollTop();
//     var div_top = $('#fixed-top-anchor').offset().top;
//     if (window_top > div_top) {
//         $('#fixed-top').addClass('fixDiv');
//         $('#fixed-top-anchor').height($('#fixed-top').outerHeight());
//     }
//     else {
//         $('#fixed-top').removeClass('fixDiv');
//         $('#fixed-top-anchor').height(0);
//     }
// }


$(function() {

/*    $('#btn-nav-mobile').on('click', function () {
        $('#site-nav-mobile').slideToggle(function() {
            $('#site-nav-mobile > ul').css('show-mobile');
        });
    });*/



	$(window).scroll(function() {
		if ($(window).scrollTop() > $('#fixed-top-anchor').offset().top) {
	    	$('#fixed-top').addClass('fixDiv');
	    	$('#books-top').addClass('book-margin-top');
	    }
	    if ($(window).scrollTop() < $('#fixed-top-anchor').offset().top) {
	      	$('#fixed-top').removeClass('fixDiv');
	      	$('#books-top').removeClass('book-margin-top');
	    }
	});



	$('#mobile-dropdown').on('click', function () {
        $('#header-mobile').slideToggle(function() {
            $('#header-mobile > ul').css('mobile-view');
        });
    });

});