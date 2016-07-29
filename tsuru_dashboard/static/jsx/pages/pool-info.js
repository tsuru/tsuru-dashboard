import React from "react";
import ReactDOM from "react-dom";
import { NodeCreate } from "../components/node-create";
import { Metrics } from "../components/metrics";

var pool = window.location.pathname.split("/")[3];

ReactDOM.render(
  <NodeCreate pool={pool} />,
  document.getElementById('node-create')
);

var pool = window.location.pathname.split('/')[3];
ReactDOM.render(
  <Metrics targetType={"pool"} targetName={pool}
    metrics={[
        "cpu_max", "cpu_wait", "load1", "load5", "load15",
        "mem_max", "disk", "swap", "nettx", "netrx"
    ]}/>,
  document.getElementById('pool-metrics')
);
