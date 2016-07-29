import React, { Component } from "react";
import oboe from "oboe";
import { ReactDOM } from "react-dom";

class Follow extends Component {
  constructor(props) {
    super(props);

    this.state = {
      lastScroll: 0
    }

    this.handleScroll = this.handleScroll.bind(this);
  }

  componentDidMount() {
    window.addEventListener('scroll', this.handleScroll);
  }

  componentWillUnmount() {
    window.removeEventListener('scroll', this.handleScroll);
  }

  handleScroll(e) {
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
  }

  render() {
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
}

class Top extends Component {
  constructor(props) {
    super(props);

    this.handleScroll = this.handleScroll.bind(this);
  }

  componentDidMount() {
    window.addEventListener('scroll', this.handleScroll);
  }

  componentWillUnmount() {
    window.removeEventListener('scroll', this.handleScroll);
  }

  handleScroll(e) {
    var scroll = window.scrollY;
    var windowSize = window.innerHeight;
    var pageSize = window.document.getElementsByTagName('body')[0].clientHeight;
    var bottom = pageSize - windowSize - scroll;
    ReactDOM.findDOMNode(this.refs.toTop).style.bottom = bottom + 'px';
  }

  render() {
    return (
      <a href="#" ref="toTop" className="to-top" onClick={this.props.onClick}>Top ▲</a>
    )
  }
}

export class Log extends Component {
  constructor(props) {
    super(props);

    this.state = {
      follow: true,
      logging: false
    }
    
    this.top = this.top.bind(this);
    this.followToggle = this.followToggle.bind(this);
  }

  top(e) {
    e.preventDefault();
    e.stopPropagation();
    this.setState({follow: false});
    window.scrollTo(0, 0);
  }

  follow() {
    window.scrollTo(0, document.body.scrollHeight);
  }

  unFollow() {
    this.setState({follow: false});
  }

  followToggle(e) {
    e.preventDefault();
    e.stopPropagation();
    var newState = !this.state.follow;
    if (newState) {
      this.follow();
    }
    this.setState({follow: newState});
  }

  componentDidMount() {
    oboe(this.props.url).done((things) => {
      this.setState({logging: true});

      $.each(things, (i, data) => {
        var msg = "<p><strong>" + data.Date + " [ " + data.Source + " ][ " + data.Unit + " ]:</strong> - " + data.Message + "</p>";
        $(".log").append("<p>" + msg + "</p>");
      });

      if (this.state.follow) {
        this.follow();
      }
    });
  }

  render() {
    return (
      <div>
      { this.state.logging ? <Follow onClick={this.followToggle} follow={this.state.follow} unFollow={this.unFollow} /> : '' }
      { this.state.logging ? <div className='log'></div> : '' }
      { this.state.logging ? <Top onClick={this.top} /> : '' }
      </div>
    )
  }
}
