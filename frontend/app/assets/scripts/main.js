console.log('\'Allo \'Allo!');




/* nav menu */
var force = false;
$(".mobile-toggle__bd").click(function(e) {
	e.preventDefault();
	$(".navbar").slideToggle(200);
	if (force) {
		$(".navbar").addClass("navbar--forced");
	} else {
		$(".navbar").removeClass("navbar--forced");
	}
	force = !force;
});

