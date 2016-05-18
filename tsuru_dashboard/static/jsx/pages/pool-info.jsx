var React = require('react'),
    ReactDOM = require('react-dom'),
    NodeCreate = require("../components/node-create.jsx"),
    Metrics = require("../components/metrics.jsx").Metrics;

ReactDOM.render(
  <NodeCreate />,
  document.getElementById('node-create')
);

var pool = window.location.pathname.split('/')[3];
ReactDOM.render(
  <Metrics targetType={"pool"} targetName={pool}
    metrics={["cpu_max", "mem_max", "disk", "swap", "nettx", "netrx"]}/>,
  document.getElementById('pool-metrics')
);

