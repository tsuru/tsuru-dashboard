(function($) {
	function first_word(suggest) {
		return function(request, response) {
          var matcher = new RegExp( "^" + $.ui.autocomplete.escapeRegex( request.term ), "i" );
          response( $.grep( suggest, function( item ){
              return matcher.test( item );
          }) );
        	}
        }
	$.first_word = first_word;
})(jQuery);