var React = require('react'),
    ReactDOM = require('react-dom'),
    Components = require("../components/component-list.jsx"),
    ComponentList = Components.ComponentList;

ReactDOM.render(
  <ComponentList url="/components/list.json" />,
  document.getElementById('list-container')
);
