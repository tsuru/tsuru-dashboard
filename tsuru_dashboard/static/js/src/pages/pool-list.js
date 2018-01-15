import React from "react"
import ReactDOM from "react-dom"

document.querySelectorAll(".pool-list").forEach(function(item) {
  let nodes = []
  try {
    nodes = JSON.parse(item.getAttribute("data-nodes"))
  } catch(e) {}

  ReactDOM.render(
    <PoolList poolName={item.getAttribute("data-pool-name")} nodes={nodes} />,
    item)
})
