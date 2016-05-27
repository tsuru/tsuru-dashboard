var React = require('react'),
    PureRenderMixin = require('react-addons-pure-render-mixin');

var Loading = React.createClass({
  mixins: [PureRenderMixin],
  getDefaultProps: function() {
    return {
        className: "loader"
    }
  },
  render: function() {
    return (
      <div className={this.props.className}>
        Loading...
      </div>
    );
  }
});

module.exports = Loading;
