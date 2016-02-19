var React = require('react');

var GraphContainer = React.createClass({
  getDefaultProps: function() {
    return {
      interval: "1m",
      from: "1h",
      processName: "",
      legend: false
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
      if (Object.keys(data.data).length === 0)
        data.data = {" ": [1,1]};

      this.renderGraph(data);
    }.bind(this));
  },
  renderGraph: function(result) {
    var $elem = $("#" + this.props.kind);
    var d = [];
    for (key in result.data) {
      d.push({
        data: result.data[key],
        lines: {show: true, fill: true},
        label: key
      });
    }
    var options = {
        xaxis: {
            mode: "time",
            timezone: "browser"
        },
        grid: {
      hoverable: true,
    },
    tooltip: {
      show: true,
      content: "%x the %s was %y"
        },
        legend: {
          position: "sw",
          show: this.props.legend
        }
    };
    $.plot($elem, d, options);
  },
  render: function() {
    this.loadData();
    var kind = this.props.kind;
    var title = this.props.title;
    var appName = this.props.appName;
    var url = "/apps/" + appName + "/metrics/details/?kind=" + kind + "&from=1h&serie=1m";
    return (
      <div className="graph-container">
        <h2>{title ? title : kind}</h2>
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
        <GraphContainer kind="cpu_max" title="cpu (%)" appName={appName} processName={this.props.processName} />
        <GraphContainer kind="mem_max" title="memory (MB)" appName={appName} processName={this.props.processName} />
        <GraphContainer kind="swap" title="swap (MB)"appName={appName} processName={this.props.processName} />
        <GraphContainer kind="connections" appName={appName} processName={this.props.processName} />
        <GraphContainer kind="units" appName={appName} processName={this.props.processName} />
        <GraphContainer kind="requests_min" title="requests min" appName={appName} />
        <GraphContainer kind="response_time" title="response time (seconds)" appName={appName} />
        <GraphContainer kind="http_methods" title="http methods" appName={appName} />
        <GraphContainer kind="status_code" title="status code" appName={appName} />
        <GraphContainer kind="nettx" appName={appName} />
        <GraphContainer kind="netrx" appName={appName} />
      </div>
    );
  }
});

module.exports = {
    Metrics: Metrics,
    GraphContainer: GraphContainer,
};
