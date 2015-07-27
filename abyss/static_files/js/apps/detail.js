(function($, window){

	var detail = function(appName, envs) {
		var allGraphs = function(appName, envs) {
			var kinds = ["mem_max", "cpu_max", "connections"];
			if (envs.hasOwnProperty("GRAPHITE_HOST") || envs.hasOwnProperty("ELASTICSEARCH_HOST")) {
				$(".metrics-container").css("display", "block");
			}

			if (envs.hasOwnProperty("ELASTICSEARCH_HOST")){
				kinds.push("response_time");
				kinds.push("requests_min");
				kinds.push("units");
			}

			$.each(kinds, function(i, kind) {
				var opts = {
					appName: appName,
					serie: "1m",
					from: "1h/h",
					hover: false,
					kind: kind,
					envs: envs
				}
				$.Graph(opts);
			});
		};

		allGraphs(appName, envs);
		$.confirmation(".btn-remove", ".remove-confirmation", appName);
	};

	$.detail = detail;

})(jQuery, window);
