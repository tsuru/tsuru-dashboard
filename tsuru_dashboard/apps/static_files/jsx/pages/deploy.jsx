var React = require('react'),
    ReactDOM = require('react-dom'),
    Components = require("../components/deploy.jsx"),
    DeployBox = Components.DeployBox,
    DeployPopin = Components.DeployPopin;

var isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);
var isSafari = /Safari/.test(navigator.userAgent) && /Apple Computer/.test(navigator.vendor);

if (isChrome || isSafari) {
  ReactDOM.render(
    <DeployBox/>,
    document.getElementById('deploy-box')
  );

  ReactDOM.render(
    <DeployPopin/>,
    document.getElementById('deploy')
  );
}
