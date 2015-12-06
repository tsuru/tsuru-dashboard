var React = require('react'),
    ReactDOM = require('react-dom'),
    Components = require("../components/list.jsx"),
    AppList = Components.AppList;

ReactDOM.render(
  <AppList url="/apps/list.json" />,
  document.getElementById('list-container')
);
