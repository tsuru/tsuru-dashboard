(function($, window){

	var normalizeUrl = function(host) {
		if (host.indexOf("http") === -1) {
			host = "http://" + host;
		}
		return host;
	}

	var graph = function(opts) {
		opts["graphiteHost"] = normalizeUrl(opts["graphiteHost"]);

		if ( typeof opts["statistic"] === "undefined" ) {
			opts["statistic"] = "maxSeries";
		}

		var url = opts["graphiteHost"] + "/render/?target=summarize(" + opts["statistic"] + "(keepLastValue(" + opts["prefix"] + "." + opts["kind"] + ")), \"" + opts["serie"] + "\", \"max\")&format=json&jsonp=?&from=-" + opts["from"];

		$.getJSON( url , function( data ) {
			var d = [];
			$.each(data, function(index, target) {
				$.each(target["datapoints"], function(index, value) {
					var v = value[0];
					if ( ( opts["kind"].indexOf("mem_max") !== -1 ) || ( opts["kind"].indexOf("recv") !== -1 ) || ( opts["kind"].indexOf("sent") !== -1 ) ) {
						v = v / ( 1024 * 1024 );
					}
					d.push({y: v, x: new Date(value[1] * 1000).getTime()});
				});
			});

			if ( $("#" + opts["id"]).parents(".graph-container").length === 0 ) {
				var label = opts["label"] ? opts["label"] : opts["kind"];
				var url = '/apps/' + opts["appName"] + '/metrics/?kind=' + opts["kind"] + '&from=' + opts["from"] + '&serie=' + opts["serie"];
				var element = '<div class="graph-container"><h2>' + label + '</h2><a href="' + url + '"><div id="' + opts["id"] + '"></div></a></div>';
				$( '#metrics' ).append(element);
			} else {
				$("#" + opts["id"]).html("");
			}
			var options = {
				element: opts["id"],
				pointSize: 0,
				smooth: true,
				data: d,
				xkey: 'x',
				ykeys: ['y'],
				ymax: opts["max"],
				labels: ['Value']
			};
			if (!opts["hover"]) {
				options["hideHover"] = "always";
			}
			new Morris.Line(options);
			window.setTimeout(graph, 60000, opts);

		});
	}

	var graphs = function(opts) {
		graph(opts);
	}

	$.Graph = graphs;


})(jQuery, window);
