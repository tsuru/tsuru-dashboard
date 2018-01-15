let $
if (typeof window.jQuery === "undefined") {
  $ = require("jquery")
} else {
  $ = window.jQuery
}

export class RequestManager {
  constructor() {
    this.queue = []
    this.concurrentRequests = 8
    this.running = 0
    this.processQueue()
  }

  add(request) {
    this.queue.push(request)
  }

  processQueue() {
    let q = Object.assign(this.queue)
    for (let i = 0; i < q.length; i++) {
      if (this.running >= this.concurrentRequests) {
        break
      }
      if (!q[i].started) {
        this.queue[i].started = true
        this.doRequest(q[i], i)
      }
    }

    window.setTimeout(this.processQueue.bind(this), 500)
  }

  doRequest(request, index) {
    let self = this
    self.running++
    $.ajax({
      type: request.method,
      url: request.url,
      success: (data) => {
        request.resolve(data)
      },
      error: (e) => {
        request.reject(e.responseText)
      },
      complete: () => {
        self.running--
      }
    })
  }
}

export class Request {
  constructor(opts) {
    this.method = opts.method || "GET"
    this.url = opts.url
    this.resolve = opts.resolve || (() => {})
    this.reject = opts.reject || (() => {})
    this.started = false
  }
}
