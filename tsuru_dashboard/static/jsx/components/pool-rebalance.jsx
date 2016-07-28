// var React = require('react'),
//     $ = require('jquery'),
//     Base = require('./base.jsx'),
//     Button = Base.Button,
//     Output = Base.Output,
//     CancelBtn = Base.CancelBtn;
//
// var PoolRebalance = React.createClass({
//   getInitialState: function() {
//     return {output: '', disabled: false};
//   },
//   rebalance: function() {
//     this.setState({disabled: true, output: 'Wait until rebalance is started.'});
//     var xhr = new XMLHttpRequest();
//     xhr.open('POST', this.props.url, true);
//     xhr.onprogress = function() {
//       this.setState({output: xhr.responseText});
//     }.bind(this);
//     xhr.onload = function() {
//         setTimeout(function() {
//             location.reload();
//         }, 2000);
//     }
//     xhr.send();
//   },
//   render: function() {
//     return (
//       <div className="pool-rebalance">
//         <div className='modal-header'>
//             <h3 id='myModalLabel'>Rebalance pool</h3>
//         </div>
//         <div className='modal-body'>
//             {this.state.output.length > 0 ? <Output message={this.state.output} /> : ''}
//         </div>
//         <div className='modal-footer'>
//             <CancelBtn disabled={this.state.disabled} />
//             <Button text="rebalance" disabled={this.state.disabled} onClick={this.rebalance} />
//         </div>
//       </div>
//     );
//   }
// });
//
// module.exports = PoolRebalance;
