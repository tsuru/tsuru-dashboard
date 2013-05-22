(function(window, $) {

	function nextStep() {
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

	function appList() {
		window.location = "/";
	}

	function createApp() {
		nextStep();
		$('.create-app').popover('show');
	}

	function deploy() {
		nextStep();
		$('iframe').attr("src", "http://ascii.io/a/3226/raw");
	}

	var actions = [appList, nextStep, deploy, nextStep, nextStep, createApp];

	/* var actions = [appList, nextStep, nextStep, nextStep, nextStep, nextStep, nextStep, createApp]; */


	var pipeline = new Pipeline(actions);

	$(".next").on("click", function(event) {
		pipeline.next();
		return false;
	});
})(window, $)
