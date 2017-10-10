import React, { Component } from "react";
import ReactDOM from "react-dom";
import { Metrics } from "./metrics";
import { Tabs} from "./base";

if(typeof window.jQuery === 'undefined') {
  var $ = require('jquery');
} else {
  var $ = window.jQuery;
}

export class NodeInfo extends Component {
    constructor(props) {
      super(props);

      this.state = {
        node: null
      }
    }

  nodeInfo() {
    $.ajax({
      type: 'GET',
      url: this.props.url,
      success: (data) => {
        this.setState({node: data.node});
      }
    });
  }

  componentDidMount() {
    this.nodeInfo();
  }

  render() {
    return (
      <div className="node-container">
        {this.state.node === null ? "" : <Node node={this.state.node} />}
      </div>
    )
  }
}

export class Node extends Component {
  constructor(props) {
    super(props);

    this.state = {
      tab: "Containers"
    }

    this.setActive = this.setActive.bind(this);
  }

  setActive(tab) {
    this.setState({tab: tab});
  }

  render() {
    var info = this.props.node.info;
    var nodeAddr = info.Address.split('/')[2].split(':')[0];
    return (
      <div className="node">
        <h1>{info.Metadata.pool} - {info.Address} - {info.Status}</h1>
        <Tabs tabs={["Containers", "Metadata", "Metrics"]} setActive={this.setActive} />
        <div className="tab-content">
          {this.state.tab === "Containers" ? <ContainersTab containers={this.props.node.containers}/> : ""}
          {this.state.tab === "Metrics" ? <MetricsTab addr={nodeAddr}/> : ""}
          {this.state.tab === "Metadata" ? <MetadataTab metadata={info.Metadata}/> : ""}
          <DeleteNodeBtn addr={info.Address} removeURL={this.props.node.nodeRemovalURL}/>
        </div>
      </div>
    )
  }
}

export class ContainersTab extends Component {
  render() {
    return (
      <div className="containers">
        <table className="table">
          <tbody>
            <tr>
              <th>ID</th>
              <th>AppName</th>
              <th>Type</th>
              <th>Process name</th>
              <th>IP</th>
              <th>HostPort</th>
              <th>Status</th>
            </tr>
            {this.props.containers.map((c) => {
              return <ContainerRow key={c.ID} container={c}/>
            })}
          </tbody>
        </table>
      </div>
    )
  }
}

export class ContainerRow extends Component {
  render() {
    var container = this.props.container;
    return (
      <tr>
        <td>{container.ID.slice(0,12)}</td>
        <td><a href={container.DashboardURL}>{container.AppName}</a></td>
        <td>{container.Type}</td>
        <td>{container.ProcessName}</td>
        <td>{container.IP}</td>
        <td>{container.HostPort}</td>
        <td>{container.Status}</td>
      </tr>
    )
  }
}

export class MetadataTab extends Component {
  render() {
    var self = this;
    return (
      <div className="metadata">
        <table className="table">
          <tbody>
            {Object.keys(self.props.metadata).map((m) => {
              return (
                <tr key={m}>
                  <td><strong>{m}</strong></td>
                  <td>{self.props.metadata[m]}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    )
  }
}

export class MetricsTab extends Component {
  render() {
    return (
      <Metrics metrics={["load", "cpu_max", "mem_max", "nettx", "netrx", "disk", "swap"]}
        targetName={this.props.addr}
        targetType={"node"}
      />
    )
  }
}

export class DeleteNodeBtn extends Component {
  constructor(props) {
    super(props);

    this.state = {
      isOnConfirmation: false
    }

    this.onClick = this.onClick.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
  }

  onClick(e) {
    e.preventDefault();
    e.stopPropagation();
    this.setState({isOnConfirmation: !this.state.isOnConfirmation});
  }

  handleCancel(e) {
    this.setState({isOnConfirmation: false});
  }

  render() {
    return (
      <div className="deleteNode">
        <a className="btn btn-danger" onClick={this.onClick}>Delete node</a>
        {this.state.isOnConfirmation === true ? <DeleteNodeConfirmation addr={this.props.addr}
          onClose={this.handleCancel} removeAction={this.props.removeURL}/> : ""}
      </div>
    )
  }
}

export class DeleteNodeConfirmation extends Component {
  constructor(props) {
    super(props);

    this.state = {
      confirmation: "",
      rebalance: true,
      destroy: true,
      isConfirmed: false
    }

    this.handleConfirmationChange = this.handleConfirmationChange.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleClose = this.handleClose.bind(this);
    this.onSubmit = this.onSubmit.bind(this);
  }

  componentDidMount() {
    var domElem = $(ReactDOM.findDOMNode(this));
    if(domElem !== undefined){
      domElem.modal('show');
    }
  }

  handleConfirmationChange(e) {
    var state = this.state;
    state.confirmation = e.target.value;
    state.isConfirmed = state.confirmation === this.props.addr;
    this.setState(state);
  }

  handleChange(e) {
    var state = this.state;
    state[e.target.name] = !state[e.target.name];
    this.setState(state);
  }

  handleClose(e) {
    e.preventDefault();
    if(this.props.onClose !== undefined) {
      this.props.onClose(e);
    }
  }

  onSubmit(e) {
    if(!this.state.isConfirmed){
      e.preventDefault();
    }
  }

  render() {
    return (
      <div id="confirmation" className="modal fade" role="dialog" aria-labelledby="myModalLabel">
        <div className="modal-dialog" role="document">
          <div className="modal-content">
            <form onSubmit={this.onSubmit} action={this.props.removeAction} method="get">
              <div className="modal-header">
                <button type="button" className="close" data-dismiss="modal" aria-hidden="true" onClick={this.handleClose}>×</button>
                <h3 id="myModalLabel">Are you sure?</h3>
              </div>
              <div className="modal-body">
                <p>This action <strong>CANNOT</strong> be undone. This will permanently delete the <strong>{this.props.addr}</strong> node.</p>
                <p>Please type in the node address to confirm.</p>
                <input type="text" className="remove-confirmation" value={this.state.confirmation} onChange={this.handleConfirmationChange}/>
                <input type="checkbox" name="rebalance" checked={this.state.rebalance} onChange={this.handleChange} value={this.state.rebalance}/>
                <label htmlFor="rebalance">rebalance?</label>
                <input type="checkbox" name="destroy" checked={this.state.destroy} onChange={this.handleChange} value={this.state.destroy}/>
                <label htmlFor="destroy">destroy machine (iaas)</label>
              </div>
              <div className="modal-footer">
                <button className="btn cancel" data-dismiss="modal" aria-hidden="true" onClick={this.handleClose}>Cancel</button>
                <button className="btn btn-danger btn-remove" disabled={!this.state.isConfirmed}>I understand the consequences, delete this node</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    )
  }
}
