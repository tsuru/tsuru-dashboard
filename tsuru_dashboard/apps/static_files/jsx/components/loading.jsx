var React = require('react'),
    PureRenderMixin = require('react-addons-pure-render-mixin');

var Loading = React.createClass({
  mixins: [PureRenderMixin],
  render: function() {
    return (
      <div className="loader">
        Loading...
      </div>
    );
  }
});

module.exports = Loading;
