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

	var getIndex = function(opts) {
		return normalizeUrl(opts["envs"]["ELASTICSEARCH_INDEX"] || ".measure-tsuru-*");
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
					"date": {
						"date_histogram": {
							"field": "@timestamp",
							"interval": "1m"
						},
						"aggs": {
							"max": {
								"max": {
									"field": "value"
								}
							},
							"min": {
								"min": {
									"field": "value"
								}
							},
							"avg": {
								"avg": {
									"field": "value"
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
		$.each(data.aggregations.date.buckets, function(index, bucket) {
			var v = bucket.max.value;
			if ((getMetric(opts).indexOf("mem_max") !== -1 ) ||
			(getMetric(opts).indexOf("recv") !== -1) ||
			(getMetric(opts).indexOf("sent") !== -1 )) {

				v = v / ( 1024 * 1024 );

			}
			d.push({x: new Date(bucket.key * 1000).getTime(), y: v});
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
			smooth: true,
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
		});

	}

	$.elasticSearchGraph = elasticSearchGraph;

})(jQuery, window);
