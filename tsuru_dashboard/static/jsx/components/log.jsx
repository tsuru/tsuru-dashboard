var React = require('react'),
	oboe = require('oboe'),
	ReactDOM = require('react-dom');

var Follow = React.createClass({
  getInitialState: function() {
    return {lastScroll: 0};
  },
  componentDidMount: function() {
    window.addEventListener('scroll', this.handleScroll);
  },
  componentWillUnmount: function() {
    window.removeEventListener('scroll', this.handleScroll);
  },
  handleScroll: function(e) {
	var scroll = window.scrollY;
	
	if (scroll < this.state.lastScroll) { 
		this.props.unFollow();
	}

	var top = window.scrollY - 230;
	if (top < 0) {
		top = 0;
	}
	
    ReactDOM.findDOMNode(this.refs.logTail).style.top = top + 'px';
	this.setState({lastScroll: window.scrollY});
  },
  render: function() {
	var classNames = "tail-status";
	if (this.props.follow) {
		classNames += " active";
	}
    return (
      <a ref="logTail" className="log-tail" href="#" onClick={this.props.onClick}>
        <span className={classNames}></span>
        <span className="tail-label">Scroll to End of Log</span>
      </a>
    )
  }
});

var Top = React.createClass({
  componentDidMount: function() {
    window.addEventListener('scroll', this.handleScroll);
  },
  componentWillUnmount: function() {
    window.removeEventListener('scroll', this.handleScroll);
  },
  handleScroll: function(e) {
	var scroll = window.scrollY;
	var windowSize = window.innerHeight;
	var pageSize = window.document.getElementsByTagName('body')[0].clientHeight;
	var bottom = pageSize - windowSize - scroll;
    ReactDOM.findDOMNode(this.refs.toTop).style.bottom = bottom + 'px';
  },
  render: function() {
    return (
      <a href="#" ref="toTop" className="to-top" onClick={this.props.onClick}>Top ▲</a>
    )
  }
});

var Log = React.createClass({
  getInitialState: function() {
    return {follow: true, logging: false};
  },
  top: function(e) {
	e.preventDefault();
    e.stopPropagation();
    this.setState({follow: false});
    window.scrollTo(0, 0);
  },
  follow: function() {
    window.scrollTo(0, document.body.scrollHeight);
  },
  unFollow: function() {
    this.setState({follow: false});
  },
  followToggle: function(e) {
	e.preventDefault();
    e.stopPropagation();
	var newState = !this.state.follow;
	if (newState) {
    	this.follow();
	}
    this.setState({follow: newState});
  },
  componentDidMount: function() {
    oboe(this.props.url).done(function(things) {
      this.setState({logging: true});

      $.each(things, function(i, data) {
        var msg = "<p><strong>" + data.Date + " [ " + data.Source + " ][ " + data.Unit + " ]:</strong> - " + data.Message + "</p>";
        $(".log").append("<p>" + msg + "</p>");
      }.bind(this));

	  if (this.state.follow) {
      	this.follow();
	  }
    }.bind(this));
  },
  render: function() {
    return (
      <div>
        { this.state.logging ? <Follow onClick={this.followToggle} follow={this.state.follow} unFollow={this.unFollow} /> : '' }
		{ this.state.logging ? <div className='log'></div> : '' }
        { this.state.logging ? <Top onClick={this.top} /> : '' }
      </div>
    )
  }
});

module.exports = Log;
