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
      legend: false
    }
  },
  componentDidMount: function() {
    $.getJSON(this.props.data_url, function(data) {
      if (Object.keys(data.data).length === 0)
        data.data = {" ": [1,1]};
      this.setState({model: data.data});
    }.bind(this));
  },
  render: function() {
    return (
      <div className="graph-container">
        <h2>{this.props.title}</h2>
        <a href={this.props.detail_url}>
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
  getDefaultProps: function() {
    return {
      interval: "1m",
      from: "1h",
      targetType: "app",
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
    var interval = this.props.interval;
    var from = this.props.from;

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
    return "/" + targetType + "s/" + targetName + "/metrics/details/?kind=" + metric + "&from=1h&serie=1m";
  },
  getGraphContainer: function(metric) {
    var id = this.props.targetName + "_" + metric;
    return (
      <GraphContainer id={id} title={this.props.titles[metric]}
        data_url={this.getMetricDataUrl(metric)}
        detail_url={this.getMetricDetailUrl(metric)}
        legend={this.props.legend} key={id}
      />
    );
  },
  render: function() {
    var self = this;
    return (
      <div className="metrics">
        {self.props.metrics.map(function(metric) {
          return self.getGraphContainer(metric);
        })}
      </div>
    );
  }
});

module.exports = {
    Metrics: Metrics,
    GraphContainer: GraphContainer,
    Graph: Graph
};
