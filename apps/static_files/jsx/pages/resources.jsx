var React = require('react'),
    ReactDOM = require('react-dom'),
    Resources = require("../components/resources.jsx");

ReactDOM.render(
  <Resources url="/apps/navegacional-status-code.json" />,
  document.getElementById('resources')
);
