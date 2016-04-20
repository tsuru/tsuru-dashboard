var React = require('react');

if(typeof window.jQuery === 'undefined') {
  var $ = require('jquery');
} else {
  var $ = window.jQuery;
}

var GraphContainer = React.createClass({
  getInitialState: function() {
    return {
      model: {}
    }
  },
  getDefaultProps: function() {
    return {
      interval: "1m",
      from: "1h",
      processName: "",
      legend: false
    }
  },
  componentDidMount: function() {
    var appName = this.props.appName;
    var kind = this.props.kind;
    var interval = this.props.interval;
    var from = this.props.from;

    var url = "/metrics/app/" + appName + "/?metric=" + kind + "&interval=" + interval + "&date_range=" + from;

    if (this.props.processName !== "") {
        url += "&process_name=" + this.props.processName;
    }
    $.getJSON(url, function(data) {
      if (Object.keys(data.data).length === 0)
        data.data = {" ": [1,1]};
      this.setState({model: data.data});
    }.bind(this));
  },
  render: function() {
    var kind = this.props.kind;
    var title = this.props.title;
    var appName = this.props.appName;
    var url = "/apps/" + appName + "/metrics/details/?kind=" + kind + "&from=1h&serie=1m";
    return (
      <div className="graph-container">
        <h2>{title ? title : kind}</h2>
        <a href={url}></a>
        <a href={url}>
          <Graph id={this.props.kind} legend={this.props.legend} model={this.state.model} />
        </a>
      </div>
    );
  }
});

var Graph = React.createClass({
  getOptions: function() {
    return {
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
    }
  },
  componentDidMount: function() {
    this.renderGraph();
  },
  componentDidUpdate: function() {
    this.renderGraph();
  },
  renderGraph: function() {
    var $elem = $("#" + this.props.id);
    var d = [];
    for (var key in this.props.model) {
      d.push({
        data: this.props.model[key],
        lines: {show: true, fill: true},
        label: key
      });
    }
    $.plot($elem, d, this.getOptions());
  },
  render: function() {
    return (
      <div id={this.props.id} className="graph"></div>
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
        <GraphContainer kind="nettx" title="net up (KB/s)" appName={appName} />
        <GraphContainer kind="netrx" title="net down (KB/s)" appName={appName} />
      </div>
    );
  }
});

module.exports = {
    Metrics: Metrics,
    GraphContainer: GraphContainer,
    Graph: Graph
};
