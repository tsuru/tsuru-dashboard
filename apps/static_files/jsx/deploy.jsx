var React = require('react');

var DeployBox = React.createClass({
  render: function() {
    return (
      <div className="deployBox">
        deploy box
      </div>
    );
  }
});

React.render(
  <DeployBox/>,
  document.getElementById('deploy-box')
);
