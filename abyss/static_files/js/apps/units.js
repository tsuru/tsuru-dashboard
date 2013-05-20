(function($) {

	var Slider = function(units) {
		this.units = units;
		var self = this;

		$('#h-slider').slider({
			orientation: "horizontal",
			value: this.units,
			range: "min",
			min: 1,
			max: 2,
			slide:  function( event, ui ) {
				$( "#units" ).html( ui.value );
				$( "input[name='units']" ).val( ui.value );
			},
			change: function( event, ui ) {
				if (ui.value !== self.units) {
					$(".apply-btn").show();
				} else {
					$(".apply-btn").hide();
				}
			}
		});
	}

	$.Slider = Slider;
})(jQuery);
