(function($, window){

	var graph = function(opts) {
		if (opts["envs"].hasOwnProperty("GRAPHITE_HOST")){
			$.graphiteGraph(opts);
		}

		if (opts["envs"].hasOwnProperty("ELASTICSEARCH_HOST")){
			$.elasticSearchGraph(opts);
		}
	}

	$.Graph = graph;

})(jQuery, window);
