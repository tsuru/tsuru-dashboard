(function($, window){

	var graph = function(kind, graphiteHost, appName, from, serie) {
		var url = "http://" + graphiteHost + "/render/?target=summarize(maxSeries(statsite.tsuru." + appName + ".*.*." + kind + "), \"" + serie + "\", \"max\")&format=json&jsonp=?&from=-" + from;
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
				var url = '/apps/xavier-qa2/metrics/?kind=' + kind + '&from=' + from + '&serie=' + serie;
				var element = '<div class="graph-container"><h2>' + kind + '</h2><a href="' + url + '"><div id="' + kind + '"></div></a></div>';
				$( '#metrics' ).append(element);
			} else {
				$("#" + kind).html("");
			}

			new Morris.Line({
				element: kind,
				pointSize: 0,
				hideHover: 'always',
				smooth: true,
				data: d,
				xkey: 'x',
				ykeys: ['y'],
				labels: ['Value']
			});

			window.setTimeout(graph, 10000, kind, graphiteHost, appName, from, serie);

		});
	}

	var graphs = function(graphiteHost, appName, kind, from, serie) {
		graph(kind, graphiteHost, appName, from, serie);
	}

	$.Graph = graphs;


})(jQuery, window);
