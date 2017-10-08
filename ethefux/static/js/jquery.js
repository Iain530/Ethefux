$(document).ready( function () {

	$(".accept-contract").on("click", function() {
		alert("click");
		var div = ".contract > "+ $(this);
		$(div).css("color", "#90ff68");
		$(this).hide();
		$(div).html += "Accepted";

	});

});
