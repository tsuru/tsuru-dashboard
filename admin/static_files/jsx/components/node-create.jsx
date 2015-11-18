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
      <div className="register">
        <label>Register an already created node: <input type="checkbox" /></label>
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
    return {};
  },
  render: function() {
    return (
      <div className="node-create">
        <h1>Create Node</h1>
        <Template />
        <Register />
        <Meta />
      </div>
    );
  }
});

module.exports = NodeCreate;
