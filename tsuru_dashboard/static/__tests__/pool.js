import React from "react"
import { mount } from "enzyme"
import { Pool, PoolNode } from "../js/src/components/pool"
import { RequestManager } from "../js/src/lib/request-manager"
import sinon from "sinon"

describe("Pool", () => {
  let defaultAddRequest

  beforeEach(() => {
    defaultAddRequest = RequestManager.prototype.add
    RequestManager.prototype.add = sinon.spy()
  })

  afterEach(() => {
    RequestManager.prototype.add = defaultAddRequest
  })

  it("renders the pool nodes", () => {
    const nodes = [
      { address: "1.2.3.4", status: "running" },
      { address: "5.6.7.8", status: "stopped" }
    ]
    const poolList = mount(
      <Pool nodes={nodes} />
    )
    const poolNodes = poolList.find(PoolNode)

    expect(poolNodes.length).toEqual(2)
    expect(poolNodes.first().props()).toEqual(nodes[0])
    expect(poolNodes.last().props()).toEqual(nodes[1])
  })

  it("renders a link with the pool name", () => {
    const pool = mount(<Pool poolName="mypool" />)
    const link = pool.find("a")
    expect(link.length).toEqual(1)
    expect(link.prop("className")).toEqual("pool-header")
    expect(link.text()).toEqual("mypool")
  })

  it("renders a header when the node doesn't have pool", () => {
    const pool = mount(<Pool />)
    const header = pool.find("h4")
    expect(header.length).toEqual(1)
    expect(header.prop("className")).toEqual("pool-header")
    expect(header.text()).toEqual("Nodes without pool")
  })

  it("fetches nodes info", () => {
    const nodes = [
      { address: "1.2.3.4", status: "running" },
      { address: "5.6.7.8", status: "stopped" },
      { address: "9.10.11.12", status: "running" }
    ]
    mount(<Pool nodes={nodes} />)

    expect(RequestManager.prototype.add.callCount).toEqual(3)
    expect(RequestManager.prototype.add.getCall(0).args[0].url).toEqual("/admin/1.2.3.4/containers/")
    expect(RequestManager.prototype.add.getCall(1).args[0].url).toEqual("/admin/5.6.7.8/containers/")
    expect(RequestManager.prototype.add.getCall(2).args[0].url).toEqual("/admin/9.10.11.12/containers/")
  })

  it("renders node info", () => {
    const node = {
      address: "1.2.3.4",
      status: "running",
      last_success: "2018-01-16 11:15",
      units_stats: {
        started: 5,
        stopped: 1,
        total: 6
      }
    }
    const table = global.document.createElement("table")
    global.document.body.appendChild(table)
    const tbody = global.document.createElement("tbody")
    table.appendChild(tbody)
    const poolNode = mount(
      <PoolNode address={node.address} status={node.status} />,
      { attachTo: tbody }
    )

    poolNode.setState({ node: { info: node }, loading: false })
    const cols = poolNode.find("td")
    expect(cols.length).toEqual(6)
    expect(cols.at(0).text()).toEqual("1.2.3.4")
    expect(cols.at(1).text()).toEqual("5")
    expect(cols.at(2).text()).toEqual("1")
    expect(cols.at(3).text()).toEqual("6")
    expect(cols.at(4).text()).toMatch(/^2018\/01\/16 11:15:00/)
    expect(cols.at(5).text()).toEqual("running")
  })
})
