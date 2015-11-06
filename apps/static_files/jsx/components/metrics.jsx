var React = require('react'),
	$ = require('jquery');

var GraphContainer = React.createClass({
  componentDidMount: function() {
    var options = {
      element: this.props.kind, 
      pointSize: 0,
      xkey: 'x',
      smooth: false,
    };
    new Morris.Line(options);
  },
  render: function() {
    return (
      <div className="graph-container">
        <h2>{this.props.kind}</h2>
        <a href="#"></a>
        <a href="#"><div id={this.props.kind}></div></a>
      </div>
    );
  }
});
var Metrics = React.createClass({
  render: function() {
    return (
      <div className="metrics">
        <GraphContainer kind="units" />
        <GraphContainer kind="cpu_max" />
        <GraphContainer kind="mem_max" />
        <GraphContainer kind="connections" />
        <GraphContainer kind="requests_min" />
        <GraphContainer kind="response_time" />
      </div>
    );
  }
});

module.exports = Metrics;
