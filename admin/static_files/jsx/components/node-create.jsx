var React = require('react'),
	$ = require('jquery');

var Template = React.createClass({
  render: function() {
    return (
      <div className="template">
        <label>Template: <select></select></label>
      </div>
    );
  }
});

var Register = React.createClass({
  render: function() {
    return (
      <div className="register" onClick={this.props.onClick}>
        <label>
          Register an already created node: 
          <input type="checkbox" />
        </label>
      </div>
    );
  }
});

var Meta = React.createClass({
  render: function() {
    return (
      <div className="meta">
        <MetaItem />
      </div>
    );
  }
});

var MetaItem = React.createClass({
  render: function() {
    return (
      <div className="meta-item">
        <label>Key: <input type="text" /></label>
        <label>Value: <input type="text" /></label>
      </div>
    );
  }
});

var NodeCreate = React.createClass({
  getInitialState: function() {
    return {templates: [], register: false, metadata: []};
  },
  registerToggle: function() {
      this.setState({register: !this.state.register});
  },
  render: function() {
    return (
      <div className="node-create">
        <h1>Create Node</h1>
        {this.state.templates.length > 0 ? <Template templates={this.state.templates} /> : ""}
        <Register register={this.state.register} onClick={this.registerToggle} />
        <Meta metatada={this.state.metadata} />
      </div>
    );
  }
});

module.exports = NodeCreate;
