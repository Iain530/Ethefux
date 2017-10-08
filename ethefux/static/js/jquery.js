$(document).ready( function () {

	$(".accept-contract").on("click", function() {
		$(this).hide();
		$(this).parent().css("background-color", "#93d666");
		$(this).parent().css("color", "#242423");


		$(this).parent().append("Accepted") ;

	});

});
