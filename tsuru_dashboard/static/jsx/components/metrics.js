import React, { Component } from "react";
import { Loading } from "./loading";

if(typeof window.jQuery === 'undefined') {
  var $ = require('jquery');
} else {
  var $ = window.jQuery;
}


export class GraphContainer extends Component {
  constructor(props) {
    super(props);

    this.state = {
      model: {},
      data_url: this.props.data_url,
      intervalID: null,
      refresh: this.props.refresh,
      renderGraph: false
    }

    this.onLoad = this.props.onLoad.bind(this);
  }

  componentDidMount() {
    this.refreshData();
  }

  componentWillReceiveProps(nextProps) {
    if(this.props.data_url !== nextProps.data_url ||
      this.props.refresh !== nextProps.refresh) {
      this.setState({
        data_url: nextProps.data_url,
        refresh: nextProps.refresh
      }, this.refreshData);
    }
  }

  componentWillUnmount() {
    if(this.state.intervalID !== null){
      clearInterval(this.state.intervalID);
    }
  }

  refreshData() {
    this.loadData(this.state.data_url);
    this.configureRefreshInterval();
  }

  loadData(url) {
    this.onLoad(true);
    $.getJSON(url, (data) => {
      this.setState({
        model: data.data,
        renderGraph: Object.keys(data.data).length > 0
      });
      this.onLoad(false);
    });
  }

  configureRefreshInterval() {
    this.setState((previousState, currentProps) => {

      if(previousState.refresh && previousState.intervalID === null) {
        return {intervalID: setInterval(this.refreshData.bind(this), 60000)};
      } else if(!previousState.refresh && previousState.intervalID !== null) {
        clearInterval(previousState.intervalID);
        return {intervalID: null};
      }

    });
  }

  render() {
    if(this.state.renderGraph){
      return (
        <div className="graph-container">
          <h2>{this.props.title}</h2>
          <Graph id={this.props.id} legend={this.props.legend} model={this.state.model} />
        </div>
      );
    } else {
      return null;
    }
  }
}

GraphContainer.propTypes = { data_url: React.PropTypes.string.isRequired }
GraphContainer.defaultProps = {
  legend: false,
  refresh: false,
  onLoad: (isLoading) => {}
}

export class Graph extends Component {
  getOptions() {
    var seriesCount = Object.keys(this.props.model).length
    var showLegend = this.props.legend && seriesCount < 10
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
        show: showLegend
      }
    }
  }

  componentDidMount() {
    this.renderGraph();
  }

  componentDidUpdate() {
    this.renderGraph();
  }

  renderGraph() {
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
  }

  render() {
    return (
      <div id={this.props.id} className="graph"></div>
    )
  }
}

export class Metrics extends Component {
  constructor(props) {
    super(props);

    this.state = {
      interval: this.props.interval,
      from: this.props.from,
      size: "small",
      legend: this.props.legend,
      refresh: true,
      graphsLoadingCount: 0
    }

    this.updateFrom = this.updateFrom.bind(this);
    this.updateInterval = this.updateInterval.bind(this);
    this.updateSize = this.updateSize.bind(this);
    this.updateRefresh = this.updateRefresh.bind(this);
    this.updateGraphLoadCount = this.updateGraphLoadCount.bind(this);
  }

  getMetricDataUrl(metric) {
    var targetType = this.props.targetType;
    var targetName = this.props.targetName;
    var interval = this.state.interval;
    var from = this.state.from;

    var url = "/metrics/" + targetType + "/" + targetName;
    url += "/?metric=" + metric + "&interval=" + interval + "&date_range=" + from;

    if(this.props.processName !== undefined) {
      url += "&process_name=" + this.props.processName;
    }

    return url;
  }

  getGraphContainer(metric) {
    var id = this.props.targetName.split('.').join('-') + "_" + metric;
    var title = this.props.titles[metric] ? this.props.titles[metric] : metric;
    return (
      <GraphContainer id={id} title={title}
        data_url={this.getMetricDataUrl(metric)}
        legend={this.state.legend} key={id}
        refresh={this.state.refresh} onLoad={this.updateGraphLoadCount}
      />
    )
  }

  updateFrom(from) {
    this.setState({from: from});
    if(this.props.onFromChange) {
      this.props.onFromChange(from);
    }
  }

  updateInterval(interval) {
    this.setState({interval: interval});
  }

  updateSize(size) {
    this.setState({size: size, legend: size === "large"});
  }

  updateRefresh(refresh) {
    this.setState({refresh: refresh});
  }

  updateGraphLoadCount(isLoading) {
    this.setState((previousState, currentProps) => {
      if(isLoading) {
        return {graphsLoadingCount: previousState.graphsLoadingCount+1};
      } else {
        return {graphsLoadingCount: previousState.graphsLoadingCount-1};
      }
    });
  }

  render() {
    var self = this;
    var className = "graphs-" + this.state.size;
    return (
      <div className="metrics">
        <div className="metrics-options">
          <TimeRangeFilter onChange={self.updateFrom}/>
          <PeriodSelector onChange={self.updateInterval}/>
          <SizeSelector onChange={self.updateSize}/>
          <AutoRefresh onChange={self.updateRefresh} checked={self.state.refresh}/>
          {self.state.graphsLoadingCount > 0 ? <Loading className={"metrics-loader"}/> : ""}
        </div>
        <div className={className}>
          {self.props.metrics.map((metric) => {
            return self.getGraphContainer(metric);
          })}
        </div>
      </div>
    )
  }
}

Metrics.defaultProps = {
  interval: "1m",
  from: "1h",
  targetType: "app",
  legend: false,
  titles: {
    cpu_max:        "cpu (%)",
    cpu_wait:       "cpu wait (%)",
    mem_max:        "memory (MB)",
    swap:           "swap (MB)",
    connections:    "connections",
    units:          "units",
    requests_min:   "requests min",
    response_time:  "response time (seconds)",
    http_methods:   "http methods",
    status_code:    "status code",
    nettx:          "net up (KB/s)",
    netrx:          "net down (KB/s)",
    disk:           "disk space on / (MB)",
    load1:          "load 1 min",
    load5:          "load 5 min",
    load15:         "load 15 min",
  },
  metrics: [
    "cpu_max", "mem_max", "swap",
    "connections", "units"
  ]
}

class TimeRangeFilter extends Component {
  constructor(props) {
    super(props);

    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    this.props.onChange(event.target.value);
  }

  render() {
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
}

class PeriodSelector extends Component {
  constructor(props) {
    super(props);

    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    this.props.onChange(event.target.value);
  }

  render() {
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
}

class SizeSelector extends Component {
  constructor(props) {
    super(props);

    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    this.props.onChange(event.target.value);
  }

  render() {
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
}

class AutoRefresh extends Component {
  constructor(props) {
    super(props);

    this.state = {
      checked: this.props.checked
    }

    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    var checked = event.target.checked;
    this.setState({checked: checked});
    this.props.onChange(checked);
  }

  render() {
    return (
      <div className="metrics-refresh">
        <input type="checkbox" name="refresh" checked={this.state.checked}
          onChange={this.handleChange} />
        <label>Auto refresh (every 60 seconds)</label>
      </div>
    )
  }
}

export class WebTransactionsMetrics extends Component {
  render() {
    return (
      <Metrics metrics={["requests_min", "response_time",
        "http_methods", "status_code", "nettx", "netrx"]}
        targetName={this.props.appName}
        targetType={"app"}
        onFromChange={this.props.onFromChange}
      />
    )
  }
}
