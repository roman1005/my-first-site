$(document).ready(function() {
	$('.InteractivePanel').mouseenter( function() {
    $(this).css("background", "lightsteelblue");
	});
	$('.InteractivePanel').mouseleave( function() {
    $(this).css("background", "azure");
	});
    $('.InteractivePanel').on( function() {
       $(this).css("color", "cadetblue");
	$('a').css("color", "cadetblue");
});
});