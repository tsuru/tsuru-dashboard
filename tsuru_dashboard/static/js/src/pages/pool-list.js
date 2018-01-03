import React, { Component } from "react"
import ReactDOM from "react-dom"

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
              <th className="col-xs-2">Host</th>
              <th className="col-xs-2">Started units</th>
              <th className="col-xs-2">Stopped units</th>
              <th className="col-xs-2">Total units</th>
              <th className="col-xs-2">Last success</th>
              <th className="col-xs-2">Status</th>
            </tr>
          </thead>
          <tbody>
            {this.props.nodes.map((node) => <PoolNode key={node.address} address={node.address} status={node.status} /> )}
          </tbody>
        </table>
      </div>
    )
  }
}

class PoolNode extends Component {
  constructor(props) {
    super(props)

    this.state = {
      node: null,
      loading: true
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
        this.setState({node: data.node, loading: false})
      }
    })
  }

  componentDidMount() {
    if (this.props.address !== "") {
      this.nodeInfo()
    }
  }

  renderTableLine(nodeInfo) {
    let cols = [
      <td className="col-xs-2">
        <a href={`/admin/${nodeInfo.address}`} title="Containers List">
          {nodeInfo.address}
        </a>
      </td>
    ]

    if (this.state.loading) {
      cols.push(
        <td colSpan="4" className="col-xs-8" style={{textAlign: "center"}}>
          <img src="/static/img/spinner.gif" />
        </td>
      )
    } else {
      cols.push(<td className="col-xs-2">{nodeInfo.units_stats.started || 0}</td>)
      cols.push(<td className="col-xs-2">{nodeInfo.units_stats.stopped || 0}</td>)
      cols.push(<td className="col-xs-2">{nodeInfo.units_stats.total || 0}</td>)
      cols.push(<td className="col-xs-2">{nodeInfo.last_success}</td>)
    }
    cols.push(<td className="col-xs-2">{nodeInfo.status}</td>)

    return (
      <tr>
        {cols}
      </tr>
    )
  }

  render() {
    if (this.state.node === null || this.state.node.info === null) {
      if (this.props.address === "") {
        return null
      }
      return this.renderTableLine({address: this.props.address, status: this.props.status})
    }
    return this.renderTableLine(this.state.node.info)
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
  )
})
