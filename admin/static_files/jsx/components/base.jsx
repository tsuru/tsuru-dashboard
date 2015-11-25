var React = require('react');

var Output = React.createClass({
  render: function() {
    return (
      <div id='output'>
        <img src="/static/img/ajax-loader.gif" />
        <div className='messages' dangerouslySetInnerHTML={{__html: this.props.message}} />
      </div>
    )
  }
});

var Button = React.createClass({
  getDefaultProps: function() {
    return {disabled: false, onClick: function(){}, type:"button"}
  },
  render: function() {
    return (
      <button type={this.props.type}
              disabled={this.props.disabled}
              onClick={this.props.onClick}
              className='btn'>
        {this.props.text}
      </button>
    );
  }
});

var CancelBtn = React.createClass({
  getDefaultProps: function() {
    return {disabled: false}
  },
  render: function() {
    return (
      <button data-dismiss='modal'
			  disabled={this.props.disabled}
              aria-hidden='true'
              className='btn'
              onClick={this.props.onClick}>
        Cancel
      </button>
    )
  }
});

var Components = {
  Button: Button,
  CancelBtn: CancelBtn
};

module.exports = Components;
