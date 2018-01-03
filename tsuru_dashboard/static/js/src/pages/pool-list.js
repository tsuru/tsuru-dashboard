import React, { Component } from "react";
import ReactDOM from "react-dom";

class PoolList extends Component {
  render() {
    return (
      <div className="panel panel-default">
        <div className="panel-heading">
          <a href={`/admin/pool/${this.props.poolName}/`} className="pool-link">
            <h4>{this.props.poolName}</h4>
          </a>
          <span>{this.props.nodes.length} nodes</span>
        </div>

        <table className="table">
          <thead>
            <tr>
              <th>Host</th>
              <th>Started units</th>
              <th>Stopped units</th>
              <th>Total units</th>
              <th>Last success</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {this.props.nodes.map((node) => <PoolNode key={node.address} address={node.address} /> )}
          </tbody>
        </table>
      </div>
    )
  }
}

class PoolNode extends Component {
  constructor(props) {
    super(props);

    this.state = {
      node: null
    }
  }

  url() {
    return `/admin/${this.props.address}/containers/`
  }

  nodeInfo() {
    $.ajax({
      type: 'GET',
      url: this.url(),
      success: (data) => {
        this.setState({node: data.node});
      }
    });
  }

  componentDidMount() {
    if (this.props.address !== "") {
      this.nodeInfo();
    }
  }

  render() {
    if (this.state.node === null || this.state.node.info === null) {
      return null
    }

    const nodeInfo = this.state.node.info
    return (
      <tr>
        <td>
          <a href={`/admin/${nodeInfo.address}`} title="Containers List">
            {nodeInfo.address}
          </a>
        </td>
        <td>{nodeInfo.units_stats.started || 0}</td>
        <td>{nodeInfo.units_stats.stopped || 0}</td>
        <td>{nodeInfo.units_stats.total || 0}</td>
        <td>{nodeInfo.last_success}</td>
        <td>{nodeInfo.status}</td>
      </tr>
    )
  }
}

document.querySelectorAll(".pool-list").forEach(function(item) {
  let nodes = []
  try {
    nodes = JSON.parse(item.getAttribute("data-nodes"))
  } catch(e) {}

  ReactDOM.render(
    <PoolList poolName={item.getAttribute("data-pool-name")} nodes={nodes} />,
    item
  );
});
