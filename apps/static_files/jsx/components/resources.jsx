var React = require('react'),
	$ = require('jquery');

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
  handleClick: function(e) {
    e.preventDefault();
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

var Graph = React.createClass({
  render: function() {
    return (
      <div className="graph-container">
        <h2>{this.props.kind}</h2>
      </div>
    );
  }
});

var Content = React.createClass({
  render: function() {
    return (
      <div className='resources-content'>
        <p>{this.props.units.length} {this.props.units.0.Status} units</p>
        <div id="metrics">
          <Graph kind="cpu" />
        </div>
      </div>
    )
  }
});

var Resources = React.createClass({
  getInitialState: function() {
    return {process: ["web", "worker"], app: {units: []}};
  },
  appInfo: function(url) {
	$.ajax({
	  type: 'GET',
	  url: this.props.url,
	  success: function(data) {
        this.setState({app: data.app});
        this.loadProcess();
	  }.bind(this)
	});
  },
  loadProcess: function() {
    var process = [];
    this.state.app.units.forEach(function(v) {
      if (process.indexOf(v) === -1)
        process.push(v);
    });
    this.setState({process: process});
  },
  getDefaultProps: function() {
    return {state: "started"};
  },
  componentDidMount: function() {
    this.appInfo();
  },
  render: function() {
    return (
      <div className="resources">
        <ProcessTabs data={this.state.process} />
        <Content units={this.state.app.units} state={this.props.state} />
      </div>
    );
  }
});

module.exports = Resources;
