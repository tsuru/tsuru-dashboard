var React = require('react'),
    Metrics = require("../components/metrics.jsx").Metrics,
    WebTransactionsMetrics = require("../components/metrics.jsx").WebTransactionsMetrics;

if(typeof window.jQuery === 'undefined') {
  var $ = require('jquery');
} else {
  var $ = window.jQuery;
}

var Resources = React.createClass({
  getInitialState: function() {
    return {app: null};
  },
  appInfo: function(url) {
    $.ajax({
  	  type: 'GET',
  	  url: this.props.url,
  	  success: function(data) {
          this.setState({app: data.app});
  	  }.bind(this)
    });
  },
  componentDidMount: function() {
    this.appInfo();
  },
  render: function() {
    return (
      <div className="resources">
        {this.state.app === null ? "" : <Resource app={this.state.app} />}
      </div>
    );
  }
});

var Tab = React.createClass({
  onClick: function(e) {
    e.preventDefault();
    e.stopPropagation();

    if (this.props.active)
      return;

    this.props.setActive(this.props.name);
  },
  render: function() {
    return (
      <li className={this.props.active ? "active" : ''}>
        <a href="#" onClick={this.onClick}>{this.props.name}</a>
      </li>
    );
  }
});

var Tabs = React.createClass({
  getInitialState: function() {
    return {active: ""};
  },
  setActive: function(name) {
    this.setState({active: name});
    this.props.setActive(name);
  },
  componentDidUpdate: function() {
    var keys = Object.keys(this.props.process);
    if ((this.state.active === "") && keys.length > 0) {
      this.setActive(keys[0]);
    }
  },
  render: function() {
    var tabs = [];
    for (process in this.props.process) {
      tabs.push(<Tab key={process}
                  name={process}
                  active={process === this.state.active}
                  setActive={this.setActive} />);
    };
    var webT = "Web transactions";
    tabs.push(
      <Tab key={webT}
        name={webT}
        active={webT === this.state.active}
        setActive={this.setActive}
      />
    );
    return (
      <ul className="nav nav-pills">
        {tabs}
      </ul>
    );
  }
});

var Tr = React.createClass({
  render: function() {
    var unit = this.props.unit;
    return (
      <tr>
        <td>{unit.ID}</td>
        <td>{unit.HostAddr}</td>
        <td>{unit.HostPort}</td>
      </tr>
    );
  }
});

var Trs = React.createClass({
  render: function() {
    var units = this.props.units;
    var trs = [];
    for (i in units) {
      trs.push(<Tr key={i} unit={units[i]} />);
    }
    return (
      <tbody>{trs}</tbody>
    );
  }
});

var ProcessInfo = React.createClass({
  getInitialState: function() {
    return {hide: true};
  },
  onClick: function(e) {
    e.preventDefault();
    e.stopPropagation();
    this.setState({hide: !this.state.hide});
  },
  render: function() {
    var units = this.props.process;
    var kind = this.props.kind;
    var classNames = "table containers-app";
    if (this.state.hide)
      classNames += " hide";
    return (
      <div className="units-toggle" onClick={this.onClick}>
        <p><a href="#">&#x25BC;</a> {units.length} {kind} units</p>
        <table className={classNames}>
          <Trs units={units} />
        </table>
      </div>
    );
  }
});

var ProcessContent = React.createClass({
  processByStatus: function() {
    var status = {};
    for (i in this.props.process) {
      var unit = this.props.process[i];
      if (!(unit.Status in status)) {
        status[unit.Status] = [];
      }
      status[unit.Status].push(unit);
    };
    return status;
  },
  render: function() {
    var info = [];
    var process = this.processByStatus()
    for (i in process) {
        info.push(<ProcessInfo key={i} process={process[i]} kind={i} />);
    };
    var processName = this.props.process[0].ProcessName;
    return (
      <div className='resources-content' id="metrics-container">
        {info}
        <Metrics targetName={this.props.appName} processName={processName} />
      </div>
    );
  }
});

var WebTransactionsContent = React.createClass({
  render: function() {
    return (
      <div className='resources-content' id="metrics-container">
        <WebTransactionsMetrics appName={this.props.appName} />
      </div>
    )
  }
});

var Resource = React.createClass({
  getInitialState: function() {
    return {process: {}, activeProcess: null, tab: null};
  },
  setActive: function(name) {
    if(this.state.process[name] !== undefined) {
      this.setState({activeProcess: this.state.process[name], tab: "process"});
    } else {
      this.setState({tab: name, activeProcess: null});
    }
  },
  unitsByProcess: function() {
    var process = {};
    for (index in this.props.app.units) {
      var unit = this.props.app.units[index];
      if (!(unit.ProcessName in process)) {
        process[unit.ProcessName] = [];
      }
      process[unit.ProcessName].push(unit);
    }
    this.setState({process: process});
  },
  componentDidMount: function() {
    this.unitsByProcess();
  },
  render: function() {
    return (
      <div>
        <Tabs process={this.state.process} setActive={this.setActive} />
        {this.state.tab === "process" ? <ProcessContent process={this.state.activeProcess} appName={this.props.app.name} /> : ""}
        {this.state.tab === "Web transactions" ? <WebTransactionsContent appName={this.props.app.name} /> : ""}
      </div>
    );
  }
});

module.exports = Resources;
