$(document).ready(function() {
	$('.popup-form').click(function () {
		console.log(this);
		$(this).children('span').hide();
		$(this).children('#form').show();
	});

	$('.text-input').keydown(function(event) {
    	if (event.which == 13) {
    		console.log($(this).val());
    		$(this).parent().prev().html($(this).val());
        	event.preventDefault();
        	$(this).parent().hide();
        	$(this).parent().prev().show();
    	}
	});

	$('.text-input').keydown(function(event) {
    	if (event.which == 27) {
        	$(this).parent().hide();
        	$(this).parent().prev().show();
    	}
	});

});