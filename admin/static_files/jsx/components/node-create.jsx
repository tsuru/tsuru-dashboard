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
    var items = [];
    var keys = Object.keys(this.props.metadata);
    keys.forEach(function(key) {
      var value = this.props.metadata[key];
      items.push(<MetaItem key={key} metaKey={key} metaValue={value} />);
    }.bind(this));
    return (
      <div className="meta">
        {items}
        <MetaItem />
      </div>
    );
  }
});

var MetaItem = React.createClass({
  getDefaultProps: function() {
    return {metaKey: "", metaValue: ""}
  },
  onChange: function() {
  },
  render: function() {
    return (
      <div className="meta-item">
        <label>Key: <input type="text" defaultValue={this.props.metaKey} onChange={this.onChange} /></label>
        <label>Value: <input type="text" defaultValue={this.props.metaValue} onChange={this.onChange} /></label>
      </div>
    );
  }
});

var Button = React.createClass({
  getDefaultProps: function() {
    return {disabled: false}
  },
  render: function() {
    return (
      <button type='submit'
              disabled={this.props.disabled}
              className='btn'>
        Create node 
      </button>
    );
  }
});

var NodeCreate = React.createClass({
  getInitialState: function() {
    return {templates: [], register: false, metadata: {}};
  },
  registerToggle: function() {
    if (!this.state.register) {
        this.addMetadata("address", "");
    } else {
        this.removeMetadata("address");
    }
    this.setState({register: !this.state.register});
  },
  addMetadata: function(key, value) {
    var metadata = this.state.metadata; 
    metadata[key] = value;
    this.setState({metadata: metadata});
  },
  removeMetadata: function(key) {
    var metadata = this.state.metadata; 
    delete metadata[key];
    this.setState({metadata: metadata});
  },
  render: function() {
    return (
      <div className="node-create">
        <h1>Create Node</h1>
        {this.state.templates.length > 0 ? <Template templates={this.state.templates} /> : ""}
        <Register register={this.state.register} onClick={this.registerToggle} />
        <Meta metadata={this.state.metadata} />
        <Button />
      </div>
    );
  }
});

module.exports = NodeCreate;
