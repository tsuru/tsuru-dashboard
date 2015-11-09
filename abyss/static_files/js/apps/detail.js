(function($, window){

	var detail = function(appName) {
		$.confirmation(".btn-remove", ".remove-confirmation", appName);
		$.confirmation(".btn-unlock", ".unlock-confirmation", appName);
	};

	$.detail = detail;

})(jQuery, window);
