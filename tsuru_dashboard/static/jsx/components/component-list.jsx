// var React = require('react'),
//     Loading = require('./loading.jsx'),
//     Metrics = require("../components/metrics.jsx").Metrics;
//
// if(typeof window.jQuery === 'undefined') {
//   var $ = require('jquery');
// } else {
//   var $ = window.jQuery;
// }
//
// var ComponentList = React.createClass({
//   getInitialState: function() {
//     return {components: [], loading: false};
//   },
//   componentDidMount: function() {
//     this.setState({loading: true});
//     $.ajax({
//       type: 'GET',
//       url: this.props.url,
//       success: function(data) {
//         this.setState({components: data.components, loading: false});
//       }.bind(this)
//     });
//   },
//   render: function() {
//     return (
//       <div className="component-list">
//         {this.state.loading ? <Loading /> : ''}
//         {this.state.components.map(function(component) {
//           return (<Component name={component} key={component}/>);
//         })}
//       </div>
//     );
//   }
// });
//
// var Component = React.createClass({
//   render: function() {
//     var metrics = ["cpu_max", "mem_max", "swap", "connections", "units", "nettx", "netrx"];
//     return (
//       <div className='component'>
//         <h2>{this.props.name}</h2>
//         <div className='metrics'>
//           <Metrics targetName={this.props.name} targetType={"component"} metrics={metrics} />
//         </div>
//       </div>
//     );
//   }
// });
//
// module.exports = {
//   ComponentList: ComponentList,
//   Component: Component
// }
