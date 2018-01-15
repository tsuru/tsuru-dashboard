import { RequestManager, Request } from "../js/src/lib/request-manager"
import sinon from "sinon"

describe("RequestManager", () => {
  var server, clock

  beforeEach(() => {
    server = sinon.fakeServer.create()
    clock = sinon.useFakeTimers()
  });

  afterEach(() => {
    clock.restore()
    server.restore()
  })

  it("sets default configs", () => {
    const rm = new RequestManager()
    expect(rm.queue.length).toEqual(0)
    expect(rm.concurrentRequests).toEqual(8)
    expect(rm.running).toEqual(0)
  });

  it("processes queued requests after 500 ms", () => {
    const rm = new RequestManager()
    const r = new Request({
      url: "test.url"
    })
    rm.add(r)

    clock.tick(501)
    server.respond()
    expect(server.requests.length).toEqual(1)
    expect(server.requests[0].url).toEqual("test.url")
  })

  it("respects maximum concurrent requests", () => {
    const rm = new RequestManager()
    rm.concurrentRequests = 2
    const r1 = new Request({
      url: "url1"
    })
    const r2 = new Request({
      url: "url2"
    })
    const r3 = new Request({
      url: "url3"
    })
    rm.add(r1)
    rm.add(r2)
    rm.add(r3)

    clock.tick(501)
    server.respond()
    expect(server.requests.length).toEqual(2)
    expect(server.requests[0].url).toEqual("url1")
    expect(server.requests[1].url).toEqual("url2")

    clock.tick(501)
    server.respond()
    expect(server.requests.length).toEqual(3)
    expect(server.requests[2].url).toEqual("url3")
  })

  it("calls requests resolve and reject callbacks", () => {
    let resolveFunc = sinon.spy()
    let rejectFunc = sinon.spy()
    const rm = new RequestManager()
    const r1 = new Request({
      url: "url1",
      resolve: resolveFunc
    })
    const r2 = new Request({
      url: "url2",
      reject: rejectFunc
    })
    rm.add(r1)
    rm.add(r2)

    server.respondWith(/url1/, [200, {}, "OK"])
    server.respondWith(/url2/, [500, {}, "error"])
    clock.tick(501)
    server.respond()
    expect(server.requests.length).toEqual(2)
    expect(resolveFunc.callCount).toEqual(1)
    expect(resolveFunc.getCall(0).args[0]).toEqual("OK")
    expect(rejectFunc.callCount).toEqual(1)
    expect(rejectFunc.getCall(0).args[0]).toEqual("error")
  })
})
