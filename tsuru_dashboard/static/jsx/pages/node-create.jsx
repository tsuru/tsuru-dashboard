var React = require('react'),
    ReactDOM = require('react-dom'),
    NodeCreate = require("../components/node-create.jsx");

var pool = window.location.pathname.split("/")[3];

ReactDOM.render(
  <NodeCreate pool={pool}/>,
  document.getElementById('node-create')
);
