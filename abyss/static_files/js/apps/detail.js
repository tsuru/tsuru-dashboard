(function($, window){

	var detail = function(appName, envs) {
		$.AllGraphs(appName, envs);
		$.confirmation(".btn-remove", ".remove-confirmation", appName);
	};

	$.detail = detail;

})(jQuery, window);
