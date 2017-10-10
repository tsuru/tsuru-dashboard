import React, { Component } from "react";
import { Metrics, WebTransactionsMetrics } from "../components/metrics";
import { TopSlow } from "../components/top-slow";
import { Tabs } from "../components/base";

if(typeof window.jQuery === 'undefined') {
  var $ = require('jquery');
} else {
  var $ = window.jQuery;
}

export class Resources extends Component {
  constructor(props) {
    super(props);

    this.state = {
      app: null
    }
  }

  appInfo(url) {
    $.ajax({
  	  type: 'GET',
  	  url: this.props.url,
  	  success: (data) => {
          this.setState({app: data.app});
  	  }
    });
  }

  componentDidMount() {
    this.appInfo();
  }

  render() {
    return (
      <div className="resources">
        {this.state.app === null ? "" : <Resource app={this.state.app} />}
      </div>
    );
  }
}

class Tr extends Component {
  render() {
    var unit = this.props.unit;
    return (
      <tr>
        <td>{unit.ID}</td>
        <td>{unit.HostAddr}</td>
        <td>{unit.HostPort}</td>
      </tr>
    );
  }
}

class Trs extends Component {
  render() {
    var units = this.props.units;
    var trs = [];
    for (let  i in units) {
      trs.push(<Tr key={i} unit={units[i]} />);
    }
    return (
      <tbody>{trs}</tbody>
    );
  }
}

class ProcessInfo extends Component {
  constructor(props) {
    super(props);

    this.state = {
      hide: true
    }

    this.onClick = this.onClick.bind(this);
  }

  onClick(e) {
    e.preventDefault();
    e.stopPropagation();
    this.setState({hide: !this.state.hide});
  }

  render() {
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
}

class ProcessContent extends Component {
  processByStatus() {
    var status = {};
    for (let i in this.props.process) {
      var unit = this.props.process[i];
      if (!(unit.Status in status)) {
        status[unit.Status] = [];
      }
      status[unit.Status].push(unit);
    };
    return status;
  }

  render() {
    var info = [];
    var process = this.processByStatus()
    for (let i in process) {
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
}

class WebTransactionsContent extends Component {
  constructor(props) {
    super(props);

    this.state = {
      from: this.props.from
    }

    this.updateFrom = this.updateFrom.bind(this);
  }

  updateFrom(from) {
    this.setState({from: from});
  }

  render() {
    return (
      <div className='resources-content' id="metrics-container">
        <WebTransactionsMetrics appName={this.props.appName} onFromChange={this.updateFrom}/>
        <TopSlow kind={"top_slow"} appName={this.props.appName} from={this.state.from}/>
      </div>
    )
  }
}

class Resource extends Component {
  constructor(props) {
    super(props);

    this.state = {
      process: {},
      activeProcess: null,
      tab: null
    }

    this.setActive = this.setActive.bind(this);
  }

  setActive(name) {
    if(this.state.process[name] !== undefined) {
      this.setState({activeProcess: this.state.process[name], tab: "process"});
    } else {
      this.setState({tab: name, activeProcess: null});
    }
  }

  unitsByProcess() {
    var process = {};
    for (let index in this.props.app.units) {
      var unit = this.props.app.units[index];
      if (!(unit.ProcessName in process)) {
        process[unit.ProcessName] = [];
      }
      process[unit.ProcessName].push(unit);
    }
    this.setState({process: process});
  }

  componentDidMount() {
    this.unitsByProcess();
  }

  render() {
    let tabs = Object.keys(this.state.process);
    if(tabs.length > 0){
      tabs.push("Web transactions");
    }
    return (
      <div>
        <Tabs tabs={tabs} setActive={this.setActive} />
        {this.state.tab === "process" ? <ProcessContent process={this.state.activeProcess} appName={this.props.app.name} /> : ""}
        {this.state.tab === "Web transactions" ? <WebTransactionsContent appName={this.props.app.name} /> : ""}
      </div>
    );
  }
}
