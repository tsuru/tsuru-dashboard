(function($, window){

	var graph = function(kind, graphiteHost, appName) {
		var url = "http://" + graphiteHost + "/render/?target=summarize(maxSeries(statsite.tsuru." + appName + ".*.*." + kind + "), \"1minute\", \"max\")&format=json&jsonp=?&from=-1h";
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

			$( "#" + kind ).remove();
			var element = '<div class="graph-container"><h2>' + kind + '</h2><div id="' + kind + '"></div></div>';
			$( '#metrics' ).append(element);

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

			window.setTimeout(graph, 60000, kind, graphiteHost, appName);

		});
	}

	var graphs = function(graphiteHost, appName) {
		var kinds = ["mem_sum", "cpu_sum", "mem_pct_sum", "mem_pct_max", "mem_max", "cpu_max"];
		$.each(kinds, function(i, kind) {
			graph(kind, graphiteHost, appName);
		});
	}

	$.Graph = graphs;


})(jQuery, window);
