(function($, window){

	var metrics = function(appName, envs) {

		var queryString = function(key) {
			var keys = {};
			var items = window.location.search.substr(1).split("&");
			$.each(items, function(i, item) {
				var keyValue = item.split("=");
				keys[keyValue[0]] = keyValue[1];
			});
			return keys[key];
		}

		$("select[name=from]").val(queryString("from"));
		$("select[name=serie]").val(queryString("serie"));
		$("input[name=kind]").val(queryString("kind"));

		var opts = {
			appName: appName,
			kind: queryString("kind"),
			serie: queryString("serie"),
			from: queryString("from"),
			hover: true,
			envs: envs
		}

		$.Graph(opts);

	};

	$.metrics = metrics;

})(jQuery, window);
