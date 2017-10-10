import React, { Component } from "react";
import oboe from "oboe";
import { ReactDOM } from "react-dom";
import Dropdown from 'backstage-dropdown';
import styles from './log.css';

if(typeof window.jQuery === 'undefined') {
  var $ = require('jquery');
} else {
  var $ = window.jQuery;
}

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

export class LogFilters extends Component {
    constructor(props) {
      super(props);
      this.state = {
        processList: null,
        unitsList: null,
        selectedSource: this.props.source,
        selectedUnit: this.props.unit,
      }
    }

    appInfo(url) {
      $.ajax({
        type: 'GET',
        url: this.props.appInfoUrl,
        success: (data) => {
            this.setState({
                processList: data.process_list,
                unitsList: data.app.units,
            });
        }
      });
    }

    componentDidMount() {
      this.appInfo();
    }

    render() {
        var processes = null;
        if (this.state.processList !== null) {
            processes = [""];
            for (var i=0; i < this.state.processList.length; i ++) {
                processes.push(this.state.processList[i]);
            }
            processes.push("tsuru");
        }
        var units = null;
        if (this.state.unitsList !== null) {
            units = [""];
            for (var i=0; i < this.state.unitsList.length; i ++) {
                units.push(this.state.unitsList[i].ID.substring(0,12));
            }
        }
        return (
            <div id="filter">
                <form action='' method='GET' ref='form'>
                    { this.state.processList === null ? '' : <Dropdown
                      placeholder='Source'
                      options={processes}
                      name='source'
                      value={this.state.selectedSource}
                      style={styles.logFilter}
                    /> }
                    { this.state.unitsList === null ? '' : <Dropdown
                      placeholder='Unit'
                      options={units}
                      name='unit'
                      value={this.state.selectedUnit}
                      style={styles.logFilter}
                    /> }
                    <button ref='btn' type='submit'>filter</button>
                </form>
            </div>
        )
    }
}

export class Log extends Component {
  constructor(props) {
    super(props);

    var url = this.props.url + "?";
    url += "source=" + this.props.source + "&";
    url += "unit=" + this.props.unit + "&";

    this.state = {
      follow: true,
      logging: false,
      url: url
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
    oboe(this.state.url).done((things) => {
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
        <LogFilters source={this.props.source} appInfoUrl={this.props.appInfoUrl} unit={this.props.unit} />
        <div id="logs">
            { this.state.logging ? <Follow onClick={this.followToggle} follow={this.state.follow} unFollow={this.unFollow} /> : '' }
            { this.state.logging ? <div className='log'></div> : '' }
            { this.state.logging ? <Top onClick={this.top} /> : '' }
        </div>
      </div>
    )
  }
}
