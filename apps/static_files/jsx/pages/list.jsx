var React = require('react'),
    Components = require("../components/list.jsx"),
    AppList = Components.AppList;

React.render(
  <AppList url="/apps/list.json" />,
  document.getElementById('list-container')
);
