var React = require('react'),
	$ = require('jquery');

var Option = React.createClass({
  render: function() {
    return (
      <option
        key={this.props.value}
        value={this.props.value}>
          {this.props.value}
      </option>
    );
  }
});

var Template = React.createClass({
  onChange: function(e) {
    this.props.selectTemplate(e.target.value);
  },
  render: function() {
    var options = [];
    this.props.templates.forEach(function(template) {
      options.push(<Option key={template.Name} value={template.Name} />);
    });
    return (
      <div className="template">
        <label>
          Template: 
          <select onChange={this.onChange}>
            <option>Select a template</option>
            {options}
          </select>
        </label>
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
          <input type="checkbox" onClick={this.onClick} />
        </label>
      </div>
    );
  }
});

var Meta = React.createClass({
  render: function() {
    var items = [];
    this.props.metadata.forEach(function(metadata) {
      items.push(<MetaItem key={metadata.id} name={metadata.key} value={metadata.value} removeMetadata={this.props.removeMetadata} editMetadata={this.props.editMetadata} />);
    }.bind(this));
    return (
      <div className="meta">
        {items}
      </div>
    );
  }
});

var MetaItem = React.createClass({
  getInitialState: function() {
    return {name: this.props.name, value: this.props.value};
  },
  getDefaultProps: function() {
    return {name: "", value: ""}
  },
  onChange: function(e) {
    this.props.editMetadata(this.state.name, this.refs.name.value, this.refs.value.value);
  },
  removeMetadata: function() {
    this.props.removeMetadata(this.refs.name.value);
  },
  componentWillReceiveProps: function(nextProps) {
    this.setState({name: nextProps.name, value: nextProps.value});
  },
  render: function() {
    return (
      <div className="meta-item">
        <label>
          Key: 
          <input type="text" name="name" ref="name" value={this.state.name} onChange={this.onChange} />
        </label>
        <label>
          Value: 
          <input type="text" name="value" ref="value" value={this.state.value} onChange={this.onChange} />
        </label>
        <button onClick={this.removeMetadata}>Remove item</button>
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
      <button type={this.props.type}
              disabled={this.props.disabled}
              className='btn'>
        {this.props.text}
      </button>
    );
  }
});

var NodeCreate = React.createClass({
  getInitialState: function() {
    function idMaker() { var initial = 0; return function() { initial++; return initial}}
    return {templates: [], register: false, metadata: [], id: 0, getId: idMaker()};
  },
  registerToggle: function() {
    if (!this.state.register) {
        this.addMetadata("address", "");
    } else {
        this.removeMetadata("address");
    }
    this.setState({register: !this.state.register});
  },
  getId: function() {
    return this.state.getId();
  },
  metaIndexByKey: function(key) {
    var index = -1;
    var meta = this.state.metadata; 
    meta.forEach(function(metadata, i) {
      if (metadata.key === key) {
        index = i;
      }
    });
    return index;
  },
  addMetadata: function(key, value) {
    var metadata = this.state.metadata; 
    var m = {key: key, value: value};
    var index = this.metaIndexByKey(key);
    if (index === -1) {
        m.id = this.getId();
        metadata.push(m);
        this.setState({metadata: metadata});
    } else {
        this.editMetadata(key, key, value);
    }
  },
  removeMetadata: function(key) {
    var index = this.metaIndexByKey(key);
    if (index === -1 )
      return;
    var meta = this.state.metadata;
    meta.splice(index, 1);
    this.setState({metadata: meta});
  },
  editMetadata: function(key, newKey, newValue) {
    var index = this.metaIndexByKey(key);
    if (index === -1)
        return;

    var metadata = this.state.metadata; 
    var m = metadata[index];
    m.key = newKey;
    m.value = newValue;
    metadata[index] = m;
    this.setState({metadata: metadata});
  },
  add: function(e) {
    e.preventDefault();
    this.addMetadata("", "");
  },
  loadTemplates: function() {
	$.ajax({
	  type: 'GET',
	  url: "/admin/templates.json",
	  success: function(data) {
        this.setState({templates: data});
	  }.bind(this)
	});
  },
  componentDidMount: function() {
    this.loadTemplates();
    this.addMetadata("", "");
  },
  selectTemplate: function(templateName) {
    this.state.templates.forEach(function(template) {
      if (template.Name === templateName) {
        template.Data.forEach(function(metaData) {
          this.addMetadata(metaData.Name, metaData.Value);
        }.bind(this));
      }
    }.bind(this));
  },
  render: function() {
    return (
      <div className="node-create">
        <h1>Create Node</h1>
        {this.state.templates.length > 0 ? <Template templates={this.state.templates} selectTemplate={this.selectTemplate} /> : ""}
        <Register register={this.state.register} onClick={this.registerToggle} />
        <Meta metadata={this.state.metadata} removeMetadata={this.removeMetadata} editMetadata={this.editMetadata} />
        <form onSubmit={this.add}>
        <Button text="New metadata" type="submit" />
        </form>
        <Button text="Create node" type="submit" />
      </div>
    );
  }
});

module.exports = NodeCreate;
