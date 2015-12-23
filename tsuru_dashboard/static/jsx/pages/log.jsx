var React = require('react'),
    ReactDOM = require('react-dom'),
    Log = require("../components/log.jsx");

var url = window.location.pathname + "stream/";
ReactDOM.render(
  <Log url={url} />,
  document.getElementById('logs')
);
