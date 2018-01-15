import React from "react"
import { mount } from "enzyme"
import { PoolList, PoolNode } from "../js/src/components/pool-list"
import { RequestManager } from "../js/src/lib/request-manager"
import sinon from "sinon"

describe("PoolList", () => {
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
      <PoolList nodes={nodes} />
    )
    const poolNodes = poolList.find(PoolNode)

    expect(poolNodes.length).toEqual(2)
    expect(poolNodes.first().props()).toEqual(nodes[0])
    expect(poolNodes.last().props()).toEqual(nodes[1])
  })

  it("fetches nodes info", () => {
    const nodes = [
      { address: "1.2.3.4", status: "running" },
      { address: "5.6.7.8", status: "stopped" },
      { address: "9.10.11.12", status: "running" }
    ]
    mount(<PoolList nodes={nodes} />)

    expect(RequestManager.prototype.add.callCount).toEqual(3)
    expect(RequestManager.prototype.add.getCall(0).args[0].url).toEqual("/admin/1.2.3.4/containers/")
    expect(RequestManager.prototype.add.getCall(1).args[0].url).toEqual("/admin/5.6.7.8/containers/")
    expect(RequestManager.prototype.add.getCall(2).args[0].url).toEqual("/admin/9.10.11.12/containers/")
  })
})
