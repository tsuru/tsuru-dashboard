// var React = require('react'),
//     Metrics = require("../components/metrics.jsx").Metrics,
//     WebTransactionsMetrics = require("../components/metrics.jsx").WebTransactionsMetrics,
//     TopSlow = require("../components/top-slow.jsx").TopSlow,
//     Tabs = require("../components/base.jsx").Tabs;
//
// if(typeof window.jQuery === 'undefined') {
//   var $ = require('jquery');
// } else {
//   var $ = window.jQuery;
// }
//
// var Resources = React.createClass({
//   getInitialState: function() {
//     return {app: null};
//   },
//   appInfo: function(url) {
//     $.ajax({
//   	  type: 'GET',
//   	  url: this.props.url,
//   	  success: function(data) {
//           this.setState({app: data.app});
//   	  }.bind(this)
//     });
//   },
//   componentDidMount: function() {
//     this.appInfo();
//   },
//   render: function() {
//     return (
//       <div className="resources">
//         {this.state.app === null ? "" : <Resource app={this.state.app} />}
//       </div>
//     );
//   }
// });
//
// var Tr = React.createClass({
//   render: function() {
//     var unit = this.props.unit;
//     return (
//       <tr>
//         <td>{unit.ID}</td>
//         <td>{unit.HostAddr}</td>
//         <td>{unit.HostPort}</td>
//       </tr>
//     );
//   }
// });
//
// var Trs = React.createClass({
//   render: function() {
//     var units = this.props.units;
//     var trs = [];
//     for (i in units) {
//       trs.push(<Tr key={i} unit={units[i]} />);
//     }
//     return (
//       <tbody>{trs}</tbody>
//     );
//   }
// });
//
// var ProcessInfo = React.createClass({
//   getInitialState: function() {
//     return {hide: true};
//   },
//   onClick: function(e) {
//     e.preventDefault();
//     e.stopPropagation();
//     this.setState({hide: !this.state.hide});
//   },
//   render: function() {
//     var units = this.props.process;
//     var kind = this.props.kind;
//     var classNames = "table containers-app";
//     if (this.state.hide)
//       classNames += " hide";
//     return (
//       <div className="units-toggle" onClick={this.onClick}>
//         <p><a href="#">&#x25BC;</a> {units.length} {kind} units</p>
//         <table className={classNames}>
//           <Trs units={units} />
//         </table>
//       </div>
//     );
//   }
// });
//
// var ProcessContent = React.createClass({
//   processByStatus: function() {
//     var status = {};
//     for (i in this.props.process) {
//       var unit = this.props.process[i];
//       if (!(unit.Status in status)) {
//         status[unit.Status] = [];
//       }
//       status[unit.Status].push(unit);
//     };
//     return status;
//   },
//   render: function() {
//     var info = [];
//     var process = this.processByStatus()
//     for (i in process) {
//         info.push(<ProcessInfo key={i} process={process[i]} kind={i} />);
//     };
//     var processName = this.props.process[0].ProcessName;
//     return (
//       <div className='resources-content' id="metrics-container">
//         {info}
//         <Metrics targetName={this.props.appName} processName={processName} />
//       </div>
//     );
//   }
// });
//
// var WebTransactionsContent = React.createClass({
//   getInitialState: function() {
//     return {
//       from: this.props.from
//     }
//   },
//   updateFrom: function(from) {
//     this.setState({from: from});
//   },
//   render: function() {
//     return (
//       <div className='resources-content' id="metrics-container">
//         <WebTransactionsMetrics appName={this.props.appName} onFromChange={this.updateFrom}/>
//         <TopSlow kind={"top_slow"} appName={this.props.appName} from={this.state.from}/>
//       </div>
//     )
//   }
// });
//
// var Resource = React.createClass({
//   getInitialState: function() {
//     return {process: {}, activeProcess: null, tab: null};
//   },
//   setActive: function(name) {
//     if(this.state.process[name] !== undefined) {
//       this.setState({activeProcess: this.state.process[name], tab: "process"});
//     } else {
//       this.setState({tab: name, activeProcess: null});
//     }
//   },
//   unitsByProcess: function() {
//     var process = {};
//     for (index in this.props.app.units) {
//       var unit = this.props.app.units[index];
//       if (!(unit.ProcessName in process)) {
//         process[unit.ProcessName] = [];
//       }
//       process[unit.ProcessName].push(unit);
//     }
//     this.setState({process: process});
//   },
//   componentDidMount: function() {
//     this.unitsByProcess();
//   },
//   render: function() {
//     tabs = Object.keys(this.state.process);
//     if(tabs.length > 0){
//       tabs.push("Web transactions");
//     }
//     return (
//       <div>
//         <Tabs tabs={tabs} setActive={this.setActive} />
//         {this.state.tab === "process" ? <ProcessContent process={this.state.activeProcess} appName={this.props.app.name} /> : ""}
//         {this.state.tab === "Web transactions" ? <WebTransactionsContent appName={this.props.app.name} /> : ""}
//       </div>
//     );
//   }
// });
//
// module.exports = Resources;
