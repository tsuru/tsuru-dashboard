(function($, window){

	var ranges = {
		"1h": "1h/h",
		"3h": "3h/h",
		"6h": "6h/h",
		"12h": "12h/h",
		"1d": "1d/d",
		"3d": "3d/d",
		"1w": "1w/w",
		"2w": "2w/w"
	}

	var getFrom = function(opts) {
		var from = opts["from"] || "1h";
		return ranges[from];
	}

	var series = {
		"1min": "1m",
		"5min": "5m",
		"15min": "15m",
		"1h": "1h",
		"6h": "6h",
		"1d": "1d"
	}

	var getSerie = function(opts) {
		var serie = opts["serie"] || "1m";
		return series[serie];
	}

	var kinds = {
		"mem_max": {"label": "memory utilization (MB)", "max": 512, "id": "mem_max", "metric": "*.*.mem_max"},
		"cpu_max": {"label": "cpu utilization (%)", "max": 100, "id": "cpu_max", "metric": "*.*.cpu_max"},
		"connections": {"label": "connections established", "max": 100, "id": "connections", "metric": "*.net.connections"},
		"response_time": {"label": "response time", "max": 20, "id": "response_time", "metric": "response_time"},
		"requests_min": {"label": "requests/min", "max": 20, "id": "requests_min", "metric": "response_time"},
		"units": {"label": "units", "max": 20, "id": "units", "metric": "cpu_max"}
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
						"filter": {
							"term": {
								"app.raw": opts["appName"]
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
									"from": "now-" + getFrom(opts),
									"to": "now"
								}
							]
						},
						"aggs": {
							"date": {
								"date_histogram": {
									"field": "@timestamp",
									"interval": getSerie(opts)
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

	var connectionsQuery = function(opts) {
		return {
			"index": getIndex(opts),
			"type": "connection",
			"body":
			{
				"query": {
					"filtered": {
						"filter": {
							"term": {
								"app.raw": opts["appName"]
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
									"from": "now-" + getFrom(opts),
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
									"connection": {"terms": {"field": "connection.raw"}}
								}
							}
						}
					}
				}
			}

		}
	}

	var requestsMinQuery = function(opts) {
		return {
			"index": getIndex(opts),
			"type": "response_time",
			"body":
			{
				"query": {
					"filtered": {
						"filter": {
							"term": {
								"app.raw": opts["appName"]
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
									"from": "now-" + getFrom(opts),
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
									"sum": {"sum": {"field": "count"}}
								}
							}
						}
					}
				}
			}
		}

	}

	var unitsQuery = function(opts) {
		return {
			"index": getIndex(opts),
			"type": "cpu_max",
			"body":
			{
				"query": {
					"filtered": {
						"filter": {
							"term": {
								"app.raw": opts["appName"]
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
									"from": "now-" + getFrom(opts),
									"to": "now-3m/m"
								}
							]
						},
						"aggs": {
							"date": {
								"date_histogram": {
									"field": "@timestamp",
									"interval": "2m"
								},
								"aggs": {
									"units": {"cardinality": {"field": "host"}}
								}
							}
						}
					}
				}
			}
		}

	}

	var processConnectionsData = function(opts, data) {
		var d = [];
		var keys = [];
		var maxValue = 0;
		var minValue = 0;
		$.each(data.aggregations.range.buckets[0].date.buckets, function(index, bucket) {
			var obj = {};
			obj["x"] = new Date(bucket.key).getTime();
			$.each(bucket.connection.buckets, function(index, bucket) {
				var size = bucket.doc_count;
				var conn = bucket.key;

				if (size < minValue) {
					minValue = size;
				}
				if (size > maxValue) {
					maxValue = size;
				}
				if (keys.indexOf(conn) === -1) {
					keys.push(conn);
				}
				obj[conn] = size.toFixed(2);
			});
			d.push(obj);
		});
		minValue = Math.round(minValue);
		maxValue = Math.ceil(maxValue);
		keys.forEach(function(key) {
			d.forEach(function(data) {
				if (!data.hasOwnProperty(key)){
					data[key] = 0;
				}
			});
		});
		return {
			data: d,
			min: minValue.toFixed(2),
			max: maxValue.toFixed(2),
			keys: keys
		}
	}

	var processUnitsData = function(opts, data) {
		var d = [];
		var maxValue = 0;
		var minValue = "init";
		$.each(data.aggregations.range.buckets[0].date.buckets, function(index, bucket) {
			var units = bucket.units.value;

			if (minValue === "init") {
				minValue = units;
			}

			if (units < minValue) {
				minValue = units;
			}

			if (units > maxValue) {
				maxValue = units;
			}
			d.push({
				x: new Date(bucket.key).getTime(),
				units: units.toFixed(2)
			});
		});
		minValue = Math.round(minValue);
		maxValue = Math.ceil(maxValue);
		return {
			data: d,
			min: minValue.toFixed(2),
			max: maxValue.toFixed(2)
		}
	}

	var processRequestsMinData = function(opts, data) {
		var d = [];
		var maxValue = 0;
		var minValue = "init";
		$.each(data.aggregations.range.buckets[0].date.buckets, function(index, bucket) {
			var sum = bucket.sum.value;

			if (minValue === "init") {
				minValue = sum;
			}

			if (sum < minValue) {
				minValue = sum;
			}

			if (sum > maxValue) {
				maxValue = sum;
			}
			d.push({
				x: new Date(bucket.key).getTime(),
				sum: sum.toFixed(2)
			});
		});
		minValue = Math.round(minValue);
		maxValue = Math.ceil(maxValue);
		return {
			data: d,
			min: minValue.toFixed(2),
			max: maxValue.toFixed(2)
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
				max: max.toFixed(2), min: min.toFixed(2), avg: avg.toFixed(2)
			});
		});
		minValue = Math.round(minValue);
		maxValue = Math.ceil(maxValue);
		return {
			data: d,
			min: minValue.toFixed(2),
			max: maxValue.toFixed(2)
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
			data: result.data,
			xkey: 'x',
			ykeys: ['max', 'min', 'avg'],
			ymax: result.max,
			ymin: result.min,
			smooth: false,
			labels: ['max', 'min', 'avg']
		};

		if (!opts["hover"]) {
			options["hideHover"] = "always";
		}

		buildContainer(opts);
		new Morris.Line(options);
	}

	var buildRequestsMinGraph = function(opts, data) {
		var result = processRequestsMinData(opts, data);
		var options = {
			element: opts["kind"],
			pointSize: 0,
			data: result.data,
			xkey: 'x',
			ykeys: ['sum'],
			ymax: result.max,
			ymin: result.min,
			smooth: false,
			labels: ['req/min']
		};

		if (!opts["hover"]) {
			options["hideHover"] = "always";
		}

		buildContainer(opts);
		new Morris.Line(options);
	}

	var buildConnectionsGraph = function(opts, data) {
		var result = processConnectionsData(opts, data);
		var options = {
			element: opts["kind"],
			pointSize: 0,
			data: result.data,
			xkey: 'x',
			ykeys: result.keys,
			ymax: result.max,
			ymin: result.min,
			smooth: false,
			labels: result.keys
		};

		if (!opts["hover"]) {
			options["hideHover"] = "always";
		}

		buildContainer(opts);
		new Morris.Line(options);
	}

	var buildUnitsGraph = function(opts, data) {
		var result = processUnitsData(opts, data);
		var options = {
			element: opts["kind"],
			pointSize: 0,
			data: result.data,
			xkey: 'x',
			ykeys: ['units'],
			ymax: result.max,
			ymin: result.min,
			smooth: false,
			labels: ['units']
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
		if (opts["kind"] === "requests_min") {
			opts["serie"] = "1min";
			query = requestsMinQuery(opts);
		}
		if (opts["kind"] === "units") {
			opts["serie"] = "3min";
			query = unitsQuery(opts);
		}
		if (opts["kind"] === "connections") {
			query = connectionsQuery(opts);
		}
		var url = elasticSearchHost(opts);

		var client = $.es.Client({hosts: url});
		client.search(query).then(function(data) {
			if (opts["kind"] === "requests_min") {
				buildRequestsMinGraph(opts, data);
				window.setTimeout(buildRequestsMinGraph, 60000, opts, data);
			} else if (opts["kind"] === "units") {
				buildUnitsGraph(opts, data);
				window.setTimeout(buildUnitsGraph, 60000, opts, data);
			} else if (opts["kind"] === "connections") {
				buildConnectionsGraph(opts, data);
				window.setTimeout(buildConnectionsGraph, 60000, opts, data);
			} else {
				buildGraph(opts, data);
				window.setTimeout(buildGraph, 60000, opts, data);
			}
		});
	}

	$.elasticSearchGraph = elasticSearchGraph;

})(jQuery, window);
