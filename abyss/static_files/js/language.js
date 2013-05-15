(function(window, $) {
	$(".language-select a").on('click', function(event) {
		event.preventDefault();
		window.document.cookie = "django_language=" + $(this).attr('href');
		window.location.reload();
	});
})(window, jQuery);

