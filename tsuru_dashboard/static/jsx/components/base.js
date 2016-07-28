import React, { Component } from "react";

class Ouput extends Component {
  render() {
    return (
      <div id='output'>
        <img src="/static/img/ajax-loader.gif" />
        <div className='messages' dangerouslySetInnerHTML={{__html: this.props.message}} />
      </div>
    )
  }
}

export class Button extends Component {
  constructor(props) {
    super(props);

    this.props = {
      disabled: false,
      onClick: () => {},
      type: "button"
    }
  }

  render() {
    return (
      <button type={this.props.type}
              disabled={this.props.disabled}
              onClick={this.props.onClick}
              className='btn'>
        {this.props.text}
      </button>
    );
  }
}

export class CancelBtn extends Component {
  constructor(props) {
      super(props);

      this.props = {
        disabled: false
      }
  }

  render() {
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
}

export class Tab extends Component {
  constructor(props) {
    super(props);

    this.onClick = this.onClick.bind(this);
  }

  onClick(e) {
    e.preventDefault();
    e.stopPropagation();

    if (this.props.active) {
      return;
    }

    if(this.props.setActive !== undefined){
      this.props.setActive(this.props.name);
    }
  }

  render() {
    return (
      <li className={this.props.active ? "active" : ''}>
        <a href="#" onClick={this.onClick}>{this.props.name}</a>
      </li>
    )
  }
}

export class Tabs extends Component {
  constructor(props) {
    super(props);

    this.state = {
      active: ""
    }
  }

  setActive(name) {
    this.setState({active: name});
    if(this.props.setActive !== undefined){
      this.props.setActive(name);
    }
  }

  componentWillReceiveProps(nextProps) {
    if ((this.state.active === "") && nextProps.tabs.length > 0) {
      this.setActive(nextProps.tabs[0]);
    }
  }

  componentDidMount() {
    if ((this.state.active === "") && this.props.tabs.length > 0) {
      this.setActive(this.props.tabs[0]);
    }
  }

  render() {
    var self = this;
    return (
      <ul className="nav nav-pills">
        {this.props.tabs.map(function(tab) {
          return <Tab key={tab}
                  name={tab}
                  active={tab === self.state.active}
                  setActive={self.setActive} />
        })}
      </ul>
    )
  }
}
