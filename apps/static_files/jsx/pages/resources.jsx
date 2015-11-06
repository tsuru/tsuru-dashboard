var React = require('react'),
    ReactDOM = require('react-dom'),
    Resources = require("../components/resources.jsx");

var url = "/apps/" + window.location.pathname.split("/")[2] + ".json";
ReactDOM.render(
  <Resources url={url} />,
  document.getElementById('resources')
);
