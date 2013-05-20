(function(window, $) {
	function Cookie(options) {
		this.options = options;
	}

	Cookie.prototype.remove = function() {
		var options = this.options.constructor();
		options.key = this.options.key;
		options.duration = -1;
		new Cookie(options).write();
	}

	Cookie.prototype.write = function(value) {
		if (this.options.duration){
			var date = new Date();
			date.setTime(date.getTime() + this.options.duration * 24 * 60 * 60 * 1000);
			value += '; expires=' + date.toGMTString();
		}
		window.document.cookie = this.options.key + '=' + value;
	}

	$(".language-select a").on('click', function(event) {
		event.preventDefault();
		var cookie = new Cookie({"key": "django_language"});
		cookie.remove();
		cookie.write($(this).attr("href"));
		window.location.reload();
	});
})(window, jQuery);

