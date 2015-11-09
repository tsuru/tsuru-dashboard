var React = require('react'),
	$ = require('jquery');

var GraphContainer = React.createClass({
  loadData: function() {
    var appName = this.props.appName;
    var kind = this.props.kind;
    var url ="/metrics/" + appName + "/?metric=" + kind + "&interval=1m&from=1h/h";
    $.getJSON(url, function(data) {
      if (data.data.length === 0)
        return;

      this.renderGraph(data);
    }.bind(this));
  },
  renderGraph: function(result) {
    var ykeys = Object.keys(result.data[0]).filter(function(value) { return value != "x" });
    var options = {
      element: this.props.kind, 
	  ykeys: ykeys,
      pointSize: 0,
      xkey: 'x',
      smooth: false,
      data: result.data,
	  ymax: result.max,
      ymin: result.min,
	  hideHover: "always",
	  labels: ykeys
    };
    new Morris.Line(options);
  },
  componentDidMount: function() {
    this.loadData();
  },
  render: function() {
    var kind = this.props.kind;
    var appName = this.props.appName;
    var url = "/apps/" + appName + "/metrics/details/?kind=" + kind + "&from=1h/h&serie=1m";
    return (
      <div className="graph-container">
        <h2>{this.props.kind}</h2>
        <a href={url}></a>
        <a href={url}><div id={this.props.kind} className="graph"></div></a>
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
