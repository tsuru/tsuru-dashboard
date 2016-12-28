import React, { Component } from "react";

const Output = () =>
  <div id='output'>
    <img src="/static/img/ajax-loader.gif" />
    <div className='messages' dangerouslySetInnerHTML={{__html: this.props.message}} />
  </div>;

export const Button = (props) =>
  <button type={props.type}
    disabled={props.disabled}
    onClick={props.onClick}
    className='btn'>
    {props.text}
  </button>;

Button.defaultProps = {
  disabled: false,
  onClick: () => {},
  type: "button"
}

export const CancelBtn = (props) =>
  <button data-dismiss='modal'
    disabled={props.disabled}
    aria-hidden='true'
    className='btn'
    onClick={props.onClick}>
    Cancel
  </button>;

CancelBtn.defaultProps = {
  disabled: false
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

    this.setActive = this.setActive.bind(this);
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
      {this.props.tabs.map((tab) => {
        return <Tab key={tab}
        name={tab}
        active={tab === self.state.active}
        setActive={self.setActive} />
      })}
      </ul>
    )
  }
}

export class Select extends Component {
  render() {
    return (
      <select>
        {this.props.defaultOption.length > 0 ? <option>{this.props.defaultOption}</option>: ""}
        {this.props.options.length > 0 ? this.props.options.map((option) => {
          return <option>{option}</option>
        }) : ""}
      </select>
    )
  }
}

Select.defaultProps = {
  defaultOption: "",
  options: []
}
