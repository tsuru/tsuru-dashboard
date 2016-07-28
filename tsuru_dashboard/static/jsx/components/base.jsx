// var React = require('react');
//
// var Output = React.createClass({
//   render: function() {
//     return (
//       <div id='output'>
//         <img src="/static/img/ajax-loader.gif" />
//         <div className='messages' dangerouslySetInnerHTML={{__html: this.props.message}} />
//       </div>
//     )
//   }
// });
//
// var Button = React.createClass({
//   getDefaultProps: function() {
//     return {disabled: false, onClick: function(){}, type:"button"}
//   },
//   render: function() {
//     return (
//       <button type={this.props.type}
//               disabled={this.props.disabled}
//               onClick={this.props.onClick}
//               className='btn'>
//         {this.props.text}
//       </button>
//     );
//   }
// });
//
// var CancelBtn = React.createClass({
//   getDefaultProps: function() {
//     return {disabled: false}
//   },
//   render: function() {
//     return (
//       <button data-dismiss='modal'
// 			  disabled={this.props.disabled}
//               aria-hidden='true'
//               className='btn'
//               onClick={this.props.onClick}>
//         Cancel
//       </button>
//     )
//   }
// });
//
// var Tab = React.createClass({
//   onClick: function(e) {
//     e.preventDefault();
//     e.stopPropagation();
//
//     if (this.props.active)
//       return;
//     if(this.props.setActive !== undefined){
//       this.props.setActive(this.props.name);
//     }
//   },
//   render: function() {
//     return (
//       <li className={this.props.active ? "active" : ''}>
//         <a href="#" onClick={this.onClick}>{this.props.name}</a>
//       </li>
//     );
//   }
// });
//
// var Tabs = React.createClass({
//   getInitialState: function() {
//     return {active: ""};
//   },
//   setActive: function(name) {
//     this.setState({active: name});
//     if(this.props.setActive !== undefined){
//       this.props.setActive(name);
//     }
//   },
//   componentWillReceiveProps: function(nextProps) {
//     if ((this.state.active === "") && nextProps.tabs.length > 0) {
//       this.setActive(nextProps.tabs[0]);
//     }
//   },
//   componentDidMount: function() {
//     if ((this.state.active === "") && this.props.tabs.length > 0) {
//       this.setActive(this.props.tabs[0]);
//     }
//   },
//   render: function() {
//     var self = this;
//     return (
//       <ul className="nav nav-pills">
//         {this.props.tabs.map(function(tab) {
//           return <Tab key={tab}
//                   name={tab}
//                   active={tab === self.state.active}
//                   setActive={self.setActive} />
//         })}
//       </ul>
//     );
//   }
// });
//
// var Components = {
//   Button: Button,
//   CancelBtn: CancelBtn,
//   Tab: Tab,
//   Tabs: Tabs
// };
//
// module.exports = Components;
