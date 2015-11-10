var React = require('react'),
	$ = require('jquery');

var GraphContainer = React.createClass({
  getInitialState: function() {
    return {
      morris: null,
    }
  },
  getDefaultProps: function() {
    return {
      interval: "1m",
      from: "1h/h",
      processName: "",
    }
  },
  loadData: function() {
    var appName = this.props.appName;
    var kind = this.props.kind;
    var interval = this.props.interval;
    var from = this.props.from;

    var url ="/metrics/" + appName + "/?metric=" + kind + "&interval=" + interval + "&date_range=" + from;

    if (this.props.processName !== "") {
        url += "&process_name=" + this.props.processName;
    }
    $.getJSON(url, function(data) {
      this.renderGraph(data);
    }.bind(this));
  },
  renderGraph: function(result) {
    $("#" + this.props.kind).empty();

    var ykeys;
    if (result.data.length > 0) {
        ykeys = Object.keys(result.data[0]).filter(function(value) { return value != "x" });
    } else {
        ykeys = ["y"];
        result.data = [{"x": 0, "y": 0}];
    }

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
  render: function() {
    this.loadData();
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
        <GraphContainer kind="cpu_max" appName={appName} processName={this.props.processName} />
        <GraphContainer kind="mem_max" appName={appName} processName={this.props.processName} />
        <GraphContainer kind="connections" appName={appName} processName={this.props.processName} />
        <GraphContainer kind="units" appName={appName} processName={this.props.processName} />
        <GraphContainer kind="requests_min" appName={appName} />
        <GraphContainer kind="response_time" appName={appName} />
      </div>
    );
  }
});

module.exports = {
    Metrics: Metrics,
    GraphContainer: GraphContainer,
};
