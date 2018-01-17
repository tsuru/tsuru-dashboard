import React from "react"
import ReactDOM from "react-dom"
import { Pool } from "../components/pool"

document.querySelectorAll(".pool-list").forEach(function(item) {
  let nodes = []
  try {
    nodes = JSON.parse(item.getAttribute("data-nodes"))
  } catch(e) {}

  ReactDOM.render(
    <Pool poolName={item.getAttribute("data-pool-name")} nodes={nodes} />,
    item)
})
