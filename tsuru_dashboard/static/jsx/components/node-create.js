import React, { Component } from "react";

if(typeof window.jQuery === 'undefined') {
  var $ = require('jquery');
} else {
  var $ = window.jQuery;
}

class Options extends Component {
  render() {
    return (
      <option
        key={this.props.value}
        value={this.props.value}>
          {this.props.value}
      </option>
    )
  }
}

class Template extends Component {
  constructor(props) {
    super(props);

    this.onChange = this.onChange.bind(this);
  }

  onChange(e) {
    this.props.selectTemplate(e.target.value);
  }

  render() {
    var options = [];

    this.props.templates.forEach((template) => {
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
    )
  }
}

class Register extends Component {
  render() {
    return (
      <div className="register" onClick={this.props.onClick}>
        <label>
          Register an already created node:
          <input type="checkbox" onClick={this.onClick} />
        </label>
      </div>
    )
  }
}

class Meta extends Component {
  render() {
    var items = [];

    this.props.metadata.forEach((metadata) => {
      items.push(<MetaItem key={metadata.id} name={metadata.key} value={metadata.value} removeMetadata={this.props.removeMetadata} editMetadata={this.props.editMetadata} />);
    });

    return (
      <div className="meta">
        {items}
      </div>
    )
  }
}

class MetaItem extends Component {
  constructor(props) {
    super(props);

    this.state = {
      name: this.props.name,
      value: this.props.value
    }

    this.onChange = this.onChange.bind(this);
  }

  onChange(e) {
    this.props.editMetadata(this.state.name, this.refs.name.value, this.refs.value.value);
  }

  removeMetadata() {
    this.props.removeMetadata(this.refs.name.value);
  }

  componentWillReceiveProps(nextProps) {
    this.setState({name: nextProps.name, value: nextProps.value});
  }

  render() {
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
    )
  }
}

MetaItem.defaultProps = {
  name: "",
  value: ""
}

class Button extends Component {
  render() {
    return (
      <button type={this.props.type}
              disabled={this.props.disabled}
              onClick={this.props.onClick}
              className='btn'>
        {this.props.text}
      </button>
    )
  }
}

Button.defaultProps = {
  disabled: false,
  onClick: () => {},
  type: "button"
}

class CancelBtn extends Component {
  render() {
    return (
      <button data-dismiss='modal'
        disabled={this.props.disabled}
              aria-hidden='true'
              className='btn'
              onClick={this.props.onClick}>
        Cancel
      </button>
    )
  }
}

CancelBtn.defaultProps = {
  disabled: false
}

class Iaas extends Component {
  constructor(props) {
    super(props);

    this.state = {
      iaas: this.props.iaas
    }

    this.onChange = this.onChange.bind(this);
  }

  onChange(e) {
    this.props.setIaas(e.target.value);
  }

  componentWillReceiveProps(nextProps) {
    this.setState({iaas: nextProps.iaas});
  }

  render() {
    return (
      <div className="iaas">
        <label>Iaas name: <input type="text" value={this.state.iaas} onChange={this.onChange} /></label>
      </div>
    );
  }
}

export class NodeCreate extends Component {
  constructor(props) {
    super(props);

    let idMaker = () => { var initial = 0; return () => { initial++; return initial}};
    this.state = {
      templates: [],
      iaas: "",
      register: false,
      metadata: [],
      id: 0,
      getId: idMaker(),
      disabled: false
    }

    this.registerToggle = this.registerToggle.bind(this);
  }

  cancel() {
    this.setState({metadata: [], register: false});
  }

  registerToggle() {
    if (!this.state.register) {
        this.addMetadata("address", "");
    } else {
        this.removeMetadata("address");
    }
    this.setState({register: !this.state.register});
  }

  getId() {
    return this.state.getId();
  }

  metaIndexByKey(key) {
    var index = -1;
    var meta = this.state.metadata;
    meta.forEach((metadata, i) => {
      if (metadata.key === key) {
        index = i;
      }
    });
    return index;
  }

  addMetadata(key, value) {
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
  }

  removeMetadata(key) {
    var index = this.metaIndexByKey(key);
    if (index === -1 )
      return;
    var meta = this.state.metadata;
    meta.splice(index, 1);
    this.setState({metadata: meta});
  }

  editMetadata(key, newKey, newValue) {
    var index = this.metaIndexByKey(key);
    if (index === -1)
        return;

    var metadata = this.state.metadata;
    var m = metadata[index];
    m.key = newKey;
    m.value = newValue;
    metadata[index] = m;
    this.setState({metadata: metadata});
  }

  add(e) {
    e.preventDefault();
    this.addMetadata("", "");
  }

  loadTemplates() {
    $.ajax({
      type: 'GET',
      url: "/admin/templates.json",
      success: (data) => {
          this.setState({templates: data});
      }
    });
  }

  componentDidMount() {
    this.loadTemplates();
  }

  selectTemplate(templateName) {
    this.state.templates.forEach((template) => {
      if (template.Name === templateName) {
        this.setIaas(template.IaaSName);
        template.Data.forEach((metaData) => {
          this.addMetadata(metaData.Name, metaData.Value);
        });
      }
    });
  }

  addNode() {
    this.setState({disabled: true});
    var url = "/admin/node/add/";
    var data = [];
    this.state.metadata.forEach((metadata) => {
      data.push("Metadata." + metadata.key + "=" + metadata.value);
    });
    if (this.state.iaas.length > 0) {
      data.push("Metadata.iaas=" + this.state.iaas);
    }
    data.push("Metadata.pool=" + this.props.pool);
    data.push("Register=" + this.state.register);
    $.ajax({
      type: "POST",
      url: url,
      data: data.join("&"),
      success: () => {
        location.reload();
      },
      error: () => {
        location.reload();
      }
    });
  }

  setIaas(iaas) {
    this.setState({iaas: iaas});
  }

  render() {
    return (
      <div className="node-create modal-dialog">
        <div className="modal-content">
          <div className='modal-header'>
            <h3 id='myModalLabel'>Create node</h3>
          </div>
          <div className='modal-body'>
            {this.state.templates != null && this.state.templates.length > 0 ? <Template templates={this.state.templates} selectTemplate={this.selectTemplate} /> : ""}
            <Register register={this.state.register} onClick={this.registerToggle} />
            <Iaas iaas={this.state.iaas} />
            <Meta metadata={this.state.metadata} removeMetadata={this.removeMetadata} editMetadata={this.editMetadata} />
          </div>
          <div className='modal-footer'>
            <CancelBtn onClick={this.cancel} disabled={this.state.disabled} />
            <Button text="Add metadata" onClick={this.add} disabled={this.state.disabled} />
            <Button text="Create node" onClick={this.addNode} disabled={this.state.disabled} />
          </div>
        </div>
      </div>
    )
  }
}
