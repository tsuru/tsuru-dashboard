var React = require('react');

var ProcessTabs = React.createClass({
  getInitialState: function() {
    return {active: ""}; 
  },
  activate: function(process) {
    this.setState({active: process});  
  },
  componentDidMount: function() {
    if (this.props.data.length > 0 && this.state.active === "") {
      this.setState({active: this.props.data[0]});
    }
  },
  render: function() {
    var processList = this.props.data.map(function(process, index) {
      return (
        <ProcessTab key={process}
                    name={process}
                    active={process === this.state.active ? true : false}
                    activate={this.activate} />
      );
    }.bind(this));
    return (
      <ul className="nav nav-pills">
        {processList}
      </ul>
    );
  }
});

var ProcessTab = React.createClass({
  handleClick: function() {
    this.props.activate(this.props.name);
  },
  render: function() {
    return (
      <li className={this.props.active ? "active" : ''}>
        <a href="#" onClick={this.handleClick}>{this.props.name}</a>
      </li>
    );
  }
});

var Resources = React.createClass({
  getInitialState: function() {
    return {process: ["web", "worker"]};
  },
  render: function() {
    return (
      <div className="resources">
        <ProcessTabs data={this.state.process} />
      </div>
    );
  }
});

module.exports = Resources;
