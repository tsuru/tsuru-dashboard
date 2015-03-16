(function($, window){

	var kinds = {
		"mem_max": {"label": "memory utilization (MB)", "max": 512, "id": "mem_max", "metric": "*.*.mem_max"},
		"cpu_max": {"label": "cpu utilization (%)", "max": 100, "id": "cpu_max", "metric": "*.*.cpu_max"},
		"connections": {"label": "connections established", "max": 100, "id": "connections", "metric": "*.net.connections"},
		"response_time": {"label": "response time", "max": 20, "id": "response_time", "metric": "response_time"}
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

	var getIndex = function(opts) {
		return opts["envs"]["ELASTICSEARCH_INDEX"] || ".measure-tsuru-*";
	}

	var buildQuery = function(opts) {
		return {
			"index": getIndex(opts),
			"type": opts["kind"],
			"body":
			{
				"query": {
					"filtered": {
						"query": {
							"match": {
								"app": opts["appName"]
							}
						}
					}
				},
				"aggs": {
					"range": {
						"date_range": {
							"field": "@timestamp",
							"ranges": [
								{
									"from": "now-1h/h",
									"to": "now"
								}
							]
						},
						"aggs": {
							"date": {
								"date_histogram": {
									"field": "@timestamp",
									"interval": "1m"
								},
								"aggs": {
									"max": {"max": {"field": "value"}},
									"min": {"min": {"field": "value"}},
									"avg": {"avg": {"field": "value"}}
								}
							}
						}
					}
				}
			}
		}

	}

	var processData = function(opts, data) {
		var d = [];
		var maxValue = 0;
		var minValue = "init";

		$.each(data.aggregations.range.buckets[0].date.buckets, function(index, bucket) {
			var max = bucket.max.value;
			var min = bucket.min.value;
			var avg = bucket.avg.value;

			if ((getMetric(opts).indexOf("mem_max") !== -1 )) {

				max = max / ( 1024 * 1024 );
				min = min / ( 1024 * 1024 );
				avg = avg / ( 1024 * 1024 );

			}

			if (minValue === "init") {
				minValue = min;
			}

			if (min < minValue) {
				minValue = min;
			}

			if (max > maxValue) {
				maxValue = max;
			}

			d.push({
				x: new Date(bucket.key).getTime(),
				max: max, min: min, avg: avg
			});
		});
		return {
			data: d,
			min: minValue,
			max: maxValue
		}
	}

	var getMax = function(opts) {
		var kind = opts["kind"];
		return kinds[kind]["max"];
	}

	var buildGraph = function(opts, data) {
		var result = processData(opts, data);
		var options = {
			element: opts["kind"],
			pointSize: 0,
			smooth: true,
			data: result.data,
			xkey: 'x',
			ykeys: ['max', 'min', 'avg'],
			ymax: result.max,
			ymin: result.min,
			labels: ['max', 'min', 'avg']
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
			var url = '/apps/' + opts["appName"] + '/metrics/?kind=' + opts["kind"] + '&from=' + opts["from"] + '&serie=' + opts["serie"];
			var element = '<div class="graph-container"><h2>' + label + '</h2><a href="' + url + '"><div id="' + opts["kind"] + '"></div></a></div>';
			$( '#metrics' ).append(element);
		} else {
			$("#" + opts["kind"]).html("");
		}
	}

	var elasticSearchHost = function(opts) {
		return normalizeUrl(opts["envs"]["ELASTICSEARCH_HOST"] || "");
	}

	var elasticSearchGraph = function(opts) {
		var query = buildQuery(opts);
		var url = elasticSearchHost(opts);

		var client = $.es.Client({hosts: url});
		client.search(query).then(function(data) {
			buildGraph(opts, data);
			window.setTimeout(buildGraph, 60000, opts, data);
		});

	}

	$.elasticSearchGraph = elasticSearchGraph;

})(jQuery, window);
