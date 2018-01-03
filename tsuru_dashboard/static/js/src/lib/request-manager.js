export class RequestManager {
  constructor() {
    this.queue = []
    this.concurrentRequests = 4
    this.running = 0
    this.processQueue()
  }

  add(request) {
    this.queue.push(request)
  }

  remove(index) {
    if (index >= 0) {
      this.queue.splice(index, 1)
    }
  }

  processQueue() {
    let q = Object.assign(this.queue)
    for (let i = 0; i < q.length; i++) {
      if (this.running >= this.concurrentRequests) {
        break
      }
      this.doRequest(q[i], i)
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
        request.reject(e)
      },
      complete: () => {
        self.running--
        self.remove(index)
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
  }
}
