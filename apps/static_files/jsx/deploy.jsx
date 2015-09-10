var React = require('react');

var DeployBox = React.createClass({
  render: function() {
    return (
      <div id="filedrag">
        drop files here to deploy
      </div>
    );
  }
});

React.render(
  <DeployBox/>,
  document.getElementById('deploy-box')
);
