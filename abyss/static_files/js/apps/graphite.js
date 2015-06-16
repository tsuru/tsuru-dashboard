(function($, window){

	var kinds = {
		"mem_max": {"label": "memory utilization (MB)", "max": 512, "id": "mem_max", "metric": "*.*.mem_max"},
		"cpu_max": {"label": "cpu utilization (%)", "max": 100, "id": "cpu_max", "metric": "*.*.cpu_max"},
		"connections": {"label": "connections established", "max": 100, "id": "connections", "metric": "*.net.connections"}
	}

  	var normalizeUrl = function(host) {
		if (host.indexOf("http") === -1) {
			host = "http://" + host;
		}
		return host;
	}

	var getMetric = function(opts) {
		var kind = opts["kind"];
		return kinds[kind]["metric"];
	}

	var buildQuery = function(opts) {
		return graphiteHost(opts) + "/render/?target=summarize(" + opts["statistic"] + "(keepLastValue(" + graphitePrefix(opts) + "." + getMetric(opts) + ")), \"" + opts["serie"] + "\", \"max\")&format=json&jsonp=?&from=-" + opts["from"];
	}

	var processData = function(opts, data) {
		var d = [];

		$.each(data, function(index, target) {
			$.each(target["datapoints"], function(index, value) {
				var v = value[0];

				if ((getMetric(opts).indexOf("mem_max") !== -1 ) ||
					(getMetric(opts).indexOf("recv") !== -1) ||
					(getMetric(opts).indexOf("sent") !== -1 )) {

					v = v / ( 1024 * 1024 );

				}

				d.push({y: v, x: new Date(value[1] * 1000).getTime()});
			});
		});

		return d;
	}

	var getMax = function(opts) {
		var kind = opts["kind"];
		return kinds[kind]["max"];
	}

	var buildGraph = function(opts, data) {

		var options = {
			element: opts["kind"],
			pointSize: 0,
			data: processData(opts, data),
			xkey: 'x',
			ykeys: ['y'],
			ymax: getMax(opts),
			labels: ['Value']
		};

		if (!opts["hover"]) {
			options["hideHover"] = "always";
		}

		buildContainer(opts);
		new Morris.Line(options);
	}

	var getLabel = function(opts) {
		var kind = opts["kind"];
		return kinds[kind]["label"];
	}

	var buildContainer = function(opts) {
		if ( $("#" + opts["kind"]).parents(".graph-container").length === 0 ) {
			var label = getLabel(opts);
			var url = '/apps/' + opts["appName"] + '/metrics/details/?kind=' + opts["kind"] + '&from=' + opts["from"] + '&serie=' + opts["serie"];
			var element = '<div class="graph-container"><h2>' + label + '</h2><a href="' + url + '"><div id="' + opts["kind"] + '"></div></a></div>';
			$( '#metrics' ).append(element);
		} else {
			$("#" + opts["kind"]).html("");
		}
	}

	var graphiteHost = function(opts) {
		return normalizeUrl(opts["envs"]["GRAPHITE_HOST"] || "");
	}

	var graphitePrefix = function(opts) {
		var graphitePrefix = opts["envs"]["GRAPHITE_PREFIX"] || "stats.gauges";
		return graphitePrefix + ".tsuru." + opts["appName"];
	}

	var graphiteGraph = function(opts) {
		var defaultOpts = {
			"statistic": "maxSeries"
		};
		opts = $.extend({}, defaultOpts, opts);

		var url = buildQuery(opts);

		$.getJSON(url , function(data) {

			buildGraph(opts, data);
			window.setTimeout(graphiteGraph, 60000, opts);


		});
	}

	$.graphiteGraph = graphiteGraph;

})(jQuery, window);
