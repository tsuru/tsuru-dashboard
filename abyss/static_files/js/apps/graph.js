(function($, window){

	var graph = function(kind, graphiteHost, appName, from, serie, hover) {
		var url = "http://" + graphiteHost + "/render/?target=summarize(maxSeries(keepLastValue(statsite.tsuru." + appName + ".*.*." + kind + ")), \"" + serie + "\", \"max\")&format=json&jsonp=?&from=-" + from;
		$.getJSON( url , function( data ) {
			var d = [];
			$.each(data, function(index, target) {
				$.each(target["datapoints"], function(index, value) {
					var v = value[0];
					if ( ( kind === "mem_sum" ) || ( kind === "mem_max" ) ) {
						v = v / ( 1024 * 1024 );
					}
					d.push({y: v, x: new Date(value[1] * 1000).getTime()});
				});
			});

			if ( $("#" + kind).parents(".graph-container").length === 0 ) {
				var url = '/apps/' + appName + '/metrics/?kind=' + kind + '&from=' + from + '&serie=' + serie;
				var element = '<div class="graph-container"><h2>' + kind + '</h2><a href="' + url + '"><div id="' + kind + '"></div></a></div>';
				$( '#metrics' ).append(element);
			} else {
				$("#" + kind).html("");
			}
			var options = {
				element: kind,
				pointSize: 0,
				smooth: true,
				data: d,
				xkey: 'x',
				ykeys: ['y'],
				labels: ['Value']
			};
			if (!hover) {
				options["hideHover"] = "always";
			}
			new Morris.Line(options);
			window.setTimeout(graph, 60000, kind, graphiteHost, appName, from, serie, hover);

		});
	}

	var graphs = function(graphiteHost, appName, kind, from, serie, hover) {
		graph(kind, graphiteHost, appName, from, serie, hover);
	}

	$.Graph = graphs;


})(jQuery, window);
