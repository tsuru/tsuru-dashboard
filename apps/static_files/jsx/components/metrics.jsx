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
    var kind = this.props.kind;
    var appName = this.props.appName;
    var url = "/apps/" + appName + "/metrics/details/?kind=" + kind + "&from=1h/h&serie=1m";
    return (
      <div className="graph-container">
        <h2>{this.props.kind}</h2>
        <a href={url}></a>
        <a href={url}><div id={this.props.kind}></div></a>
      </div>
    );
  }
});

var Metrics = React.createClass({
  render: function() {
    var appName = this.props.appName;
    return (
      <div className="metrics">
        <GraphContainer kind="units" appName={appName} />
        <GraphContainer kind="cpu_max" appName={appName} />
        <GraphContainer kind="mem_max" appName={appName} />
        <GraphContainer kind="connections" appName={appName} />
        <GraphContainer kind="requests_min" appName={appName} />
        <GraphContainer kind="response_time" appName={appName} />
      </div>
    );
  }
});

module.exports = Metrics;
