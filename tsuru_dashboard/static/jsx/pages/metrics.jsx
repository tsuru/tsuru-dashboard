var React = require('react'),
    ReactDOM = require('react-dom'),
    Metrics = require("../components/metrics.jsx").Metrics;

var appName = window.location.pathname.split("/")[2];
ReactDOM.render(
  <Metrics appName={appName} />,
  document.getElementById('metrics-container')
);
