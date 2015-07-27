(function($, window){

	var buildGraph = function(opts, result) {
        var ykeys = Object.keys(result.data[0]).filter(function(value) { return value != "x" });
		var options = {
			element: opts["kind"],
			pointSize: 0,
			data: result.data,
			xkey: 'x',
			ykeys: ykeys,
			ymax: result.max,
			ymin: result.min,
			smooth: false,
			labels: ykeys
		};

		if (!opts["hover"]) {
			options["hideHover"] = "always";
		}

		buildContainer(opts);
		new Morris.Line(options);
	}

	var buildContainer = function(opts) {
		if ( $("#" + opts["kind"]).parents(".graph-container").length === 0 ) {
			var label = opts["kind"];//getLabel(opts);
			var url = '/apps/' + opts["appName"] + '/metrics/details/?kind=' + opts["kind"] + '&from=' + opts["from"] + '&serie=' + opts["serie"];
			var element = '<div class="graph-container"><h2>' + label + '</h2><a href="' + url + '"><div id="' + opts["kind"] + '"></div></a></div>';
			$( '#metrics' ).append(element);
		} else {
			$("#" + opts["kind"]).html("");
		}
	}

	var newGraph = function(opts) {
        var url ="/metrics/" + opts.appName + "/?metric=" + opts.kind;
        $.getJSON(url, function(data) {
            buildGraph(opts, data);
			//window.setTimeout(buildGraph, 60000, opts, data);
        });
	}

	var graph = function(opts) {
        newGraph(opts);
	}

	$.Graph = graph;

})(jQuery, window);
