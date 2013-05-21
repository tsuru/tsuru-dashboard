(function(window, $) {

	function next() {
		var $container = $(".active");
		$container.removeClass("active");
		$container.next().addClass("active");
	}

	function Pipeline(actions) {
		this.actions = actions;
	}

	Pipeline.prototype.next = function() {
		if (this.actions.length > 0) {
			var action = this.actions.pop();
			action.call()
		}
	}

	var actions = [next, next, next, next, next, next, next, next];

	var pipeline = new Pipeline(actions);

	$(".next").on("click", function(event) {
		pipeline.next();
		return false;
	});
})(window, $)
