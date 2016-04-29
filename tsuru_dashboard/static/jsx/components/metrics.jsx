var React = require('react');

if(typeof window.jQuery === 'undefined') {
  var $ = require('jquery');
} else {
  var $ = window.jQuery;
}

var GraphContainer = React.createClass({
  getInitialState: function() {
    return {
      model: {},
      detail_url: this.props.detail_url
    }
  },
  getDefaultProps: function() {
    return {
      legend: false
    }
  },
  componentDidMount: function() {
    this.loadData(this.props.data_url);
  },
  componentWillReceiveProps: function(nextProps) {
    var state = this.state;
    state.detail_url = nextProps.detail_url;
    this.setState(state);
    this.loadData(nextProps.data_url);
  },
  loadData: function(url) {
    $.getJSON(url, function(data) {
      if (Object.keys(data.data).length === 0)
        data.data = {" ": [1,1]};
      var state = this.state;
      state.model = data.data;
      this.setState(state);
    }.bind(this));
  },
  render: function() {
    return (
      <div className="graph-container">
        <h2>{this.props.title}</h2>
        <a href={this.state.detail_url}>
          <Graph id={this.props.id} legend={this.props.legend} model={this.state.model} />
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
  getInitialState: function() {
    return {
      "interval": this.props.interval,
      "from": this.props.from,
      "size": "small",
      "legend": this.props.legend
    }
  },
  getDefaultProps: function() {
    return {
      interval: "1m",
      from: "1h",
      targetType: "app",
      legend: false,
      titles: {
        cpu_max: "cpu (%)",
        mem_max: "memory (MB)",
        swap: "swap (MB)",
        connections: "connections",
        units: "units",
        requests_min: "requests min",
        response_time: "response time (seconds)",
        http_methods: "http methods",
        status_code: "status code",
        nettx: "net up (KB/s)",
        netrx: "net down (KB/s)"
      },
      metrics: [
        "cpu_max", "mem_max", "swap",
        "connections", "units",
        "requests_min", "response_time",
        "http_methods", "status_code",
        "nettx", "netrx"
      ]
    }
  },
  filterByProcess: function(metric) {
    var webTransactions = ["requests_min", "response_time",
        "http_methods", "status_code",
        "nettx", "netrx"
    ];
    if ($.inArray(metric, webTransactions) === -1) {
        return "&process_name=" + this.props.processName;
    }
    return "";
  },
  getMetricDataUrl: function(metric) {
    var targetType = this.props.targetType;
    var targetName = this.props.targetName;
    var interval = this.state.interval;
    var from = this.state.from;

    var url = "/metrics/" + targetType + "/" + targetName;
    url += "/?metric=" + metric + "&interval=" + interval + "&date_range=" + from;

    if(this.props.processName !== undefined) {
      url += this.filterByProcess(metric);
    }

    return url;
  },
  getMetricDetailUrl: function(metric) {
    var targetName = this.props.targetName;
    var targetType = this.props.targetType;
    var interval = this.state.interval;
    var from = this.state.from;

    var url = "/" + targetType + "s/" + targetName + "/metrics/details";
    url += "/?kind=" + metric + "&from=" + from + "&serie=" + interval;

    return url;
  },
  getGraphContainer: function(metric) {
    var id = this.props.targetName + "_" + metric;
    return (
      <GraphContainer id={id} title={this.props.titles[metric]}
        data_url={this.getMetricDataUrl(metric)}
        detail_url={this.getMetricDetailUrl(metric)}
        legend={this.state.legend} key={id}
      />
    );
  },
  updateFrom: function(from) {
    var newState = this.state;
    newState.from = from;
    this.setState(newState);
  },
  updateInterval: function(interval) {
    var newState = this.state;
    newState.interval = interval;
    this.setState(newState);
  },
  updateSize: function(size) {
    var newState = this.state;
    newState.size = size;
    newState.legend = size === "large";
    this.setState(newState);
  },
  render: function() {
    var self = this;
    var className = "graphs-" + this.state.size;
    return (
      <div className="metrics">
        <div className="metrics-options">
          <TimeRangeFilter onChange={self.updateFrom}/>
          <PeriodSelector onChange={self.updateInterval}/>
          <SizeSelector onChange={self.updateSize}/>
        </div>
        <div className={className}>
          {self.props.metrics.map(function(metric) {
            return self.getGraphContainer(metric);
          })}
        </div>
      </div>
    );
  }
});

var TimeRangeFilter = React.createClass({
  handleChange: function(event) {
    this.props.onChange(event.target.value);
  },
  render: function() {
    return (
      <div className="metrics-range">
        <label>Time range:</label>
        <select name="from" onChange={this.handleChange}>
          <option value="1h">last hour</option>
          <option value="3h">last 3 hours</option>
          <option value="6h">last 6 hours</option>
          <option value="12h">last 12 hours</option>
          <option value="1d">last 24 hours</option>
          <option value="3d">last 3 days</option>
          <option value="1w">last 1 week</option>
          <option value="2w">last 2 weeks</option>
        </select>
      </div>
    )
  }
});

var PeriodSelector = React.createClass({
  handleChange: function(event) {
    this.props.onChange(event.target.value);
  },
  render: function() {
    return (
      <div className="metrics-period">
        <label>Period:</label>
        <select name="serie" onChange={this.handleChange}>
          <option value="1m">1 minute</option>
          <option value="5m">5 minutes</option>
          <option value="15m">15 minutes</option>
          <option value="1h">1 hour</option>
          <option value="6h">6 hours</option>
          <option value="1d">1 day</option>
        </select>
      </div>
    )
  }
});

var SizeSelector = React.createClass({
  handleChange: function(event) {
    this.props.onChange(event.target.value);
  },
  render: function() {
    return (
      <div className="metrics-size">
        <label>Size:</label>
        <select name="size" onChange={this.handleChange}>
          <option value="small">Small</option>
          <option value="medium">Medium</option>
          <option value="large">Large</option>
        </select>
      </div>
    )
  }
});

module.exports = {
    Metrics: Metrics,
    GraphContainer: GraphContainer,
    Graph: Graph
};
