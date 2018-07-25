import React, { Component } from "react"
import ReactDOM from "react-dom"
import { RequestManager, Request } from "../lib/request-manager"
import moment from "moment"

let Requests = new RequestManager()

export class Pool extends Component {
  renderPoolName() {
    if (this.props.poolName) {
      return (
        <a href={`/admin/pool/${this.props.poolName}/`} className="pool-header">
          <h4>{this.props.poolName}</h4>
        </a>
      )
    } else {
      return <h4 className="pool-header">Nodes without pool</h4>
    }
  }

  render() {
    return (
      <div className="panel panel-default">
        <div className="panel-heading">
          { this.renderPoolName() }
          <span>{this.props.nodes.length} nodes</span>
        </div>

        <table className="table text-center">
          <thead>
            <tr>
              <th className="col-xs-2 text-center">Host</th>
              <th className="col-xs-2 text-center">Started units</th>
              <th className="col-xs-2 text-center">Stopped units</th>
              <th className="col-xs-2 text-center">Total units</th>
              <th className="col-xs-2 text-center">Last success</th>
              <th className="col-xs-2 text-center">Status</th>
            </tr>
          </thead>
          <tbody>
            {this.props.nodes.map((node) => <PoolNode key={`${node.address}-node`} address={node.address} status={node.status} /> )}
          </tbody>
        </table>
      </div>
    )
  }
}

Pool.defaultProps = {
  poolName: "",
  nodes: []
}

export class PoolNode extends Component {
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
    const request = new Request({
      method: "GET",
      url: this.url(),
      resolve: (data) => {
        this.setState({node: data.node, loading: false})
      }
    })
    Requests.add(request)
  }

  componentDidMount() {
    if (this.props.address !== "") {
      this.nodeInfo()
    }
  }

  formatDate(dateStr) {
    const m = moment(dateStr)
    if (m.isValid()) {
      return m.format("YYYY/MM/DD hh:mm:ss ZZ")
    }
    return ""
  }

  renderTableLine(nodeInfo) {
    let cols = [
      <td key={`${nodeInfo.address}-col0`} className="col-xs-2 text-left">
        <a href={`/admin/${nodeInfo.address}/`} title="Containers List">
          {nodeInfo.address}
        </a>
      </td>
    ]

    if (this.state.loading) {
      cols.push(
        <td key={`${nodeInfo.address}-col${cols.length}`} colSpan="4" className="col-xs-8">
          <img src="/static/img/spinner.gif" />
        </td>
      )
    } else {
      cols.push(<td key={`${nodeInfo.address}-col${cols.length}`} className="col-xs-2">{nodeInfo.units_stats.started || 0}</td>)
      cols.push(<td key={`${nodeInfo.address}-col${cols.length}`} className="col-xs-2">{nodeInfo.units_stats.stopped || 0}</td>)
      cols.push(<td key={`${nodeInfo.address}-col${cols.length}`} className="col-xs-2">{nodeInfo.units_stats.total || 0}</td>)
      cols.push(<td key={`${nodeInfo.address}-col${cols.length}`} className="col-xs-2">{this.formatDate(nodeInfo.last_success)}</td>)
    }
    cols.push(<td key={`${nodeInfo.address}-col${cols.length}`} className="col-xs-2">{nodeInfo.status}</td>)

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
