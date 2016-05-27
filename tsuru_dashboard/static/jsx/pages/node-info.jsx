var React = require('react'),
    ReactDOM = require('react-dom'),
    NodeInfo = require("../components/node-info.jsx").NodeInfo;

var url = window.location.pathname + "containers";
ReactDOM.render(
  <NodeInfo url={url} />,
  document.getElementById('node-info')
);
