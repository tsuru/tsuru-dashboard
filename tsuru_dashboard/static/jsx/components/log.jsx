var React = require('react');
var oboe = require('oboe');

var Log = React.createClass({
  componentDidMount: function() {
    console.log(oboe);
    oboe(this.props.url).done(function(things) {
      $.each(things, function(i, data) {
        var msg = "<p><strong>" + data.Date + " [ " + data.Source + " ][ " + data.Unit + " ]:</strong> - " + data.Message + "</p>";
        $(".log").append("<p>" + msg + "</p>");
      }.bind(this));
    }.bind(this));
  },
  render: function() {
    return (
      <div className='log'></div>
    )
  }
});

module.exports = Log;
