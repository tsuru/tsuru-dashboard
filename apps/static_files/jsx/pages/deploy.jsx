var React = require('react'),
    Components = require("../components/deploy.jsx"),
    DeployBox = Components.DeployBox,
    DeployPopin = Components.DeployPopin;

React.render(
  <DeployBox/>,
  document.getElementById('deploy-box')
);

React.render(
  <DeployPopin/>,
  document.getElementById('deploy')
);
