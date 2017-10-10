import React, { Component } from "react";

class OptionItem extends Component {
  render() {
    return (
      <div className='options-item'>
        <li><a href="#">{this.props.item}</a></li>
      </div>
    )
  }
}

class OptionItems extends Component {
  render() {
    var items = this.props.items.map((item) => {
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
}

export class OptionsMenu extends Component {
  render() {
    return (
      <div className='options-menu'>
        <a href="#">...</a>
        <OptionItems items={this.props.items} />
      </div>
    )
  }
}

OptionsMenu.defaultProps = {
  items: []
}
