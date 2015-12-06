var React = require('react');

var OptionItem = React.createClass({
  render: function() {
    return (
      <div className='options-item'>
        <li><a href="#">{this.props.item}</a></li>
      </div>
    )
  }
});

var OptionItems = React.createClass({
  render: function() {
    var items = this.props.items.map(function(item) {
      return <OptionItem key={item} item={item} />
    });
    return (
      <div className='options-items'>
        <ul>
          {items}
        </ul>
      </div>
    )
  }
});

var OptionsMenu = React.createClass({
  getDefaultProps: function() {
    return {items: []};
  },
  render: function() {
    return (
      <div className='options-menu'>
        <a href="#">...</a>
        <OptionItems items={this.props.items} />
      </div>
    )
  }
});

module.exports = OptionsMenu;
