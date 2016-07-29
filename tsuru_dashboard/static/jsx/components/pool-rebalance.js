import React, { Component } from "react";
import { Button, Output, CancelBtn } from "./base";

if(typeof window.jQuery === 'undefined') {
  var $ = require('jquery');
} else {
  var $ = window.jQuery;
}

export class PoolRebalance extends Component {
  constructor(props) {
    super(props);

    this.state = {
      output: "",
      disabled: false
    }

    this.rebalance = this.rebalance.bind(this);
  }

  rebalance() {
    this.setState({disabled: true, output: 'Wait until rebalance is started.'});
    var xhr = new XMLHttpRequest();
    xhr.open('POST', this.props.url, true);
    xhr.onprogress = () => {
      this.setState({output: xhr.responseText});
    };
    xhr.onload = () => {
        setTimeout(() => {
            location.reload();
        }, 2000);
    }
    xhr.send();
  }

  render() {
    return (
      <div className="pool-rebalance">
        <div className='modal-header'>
            <h3 id='myModalLabel'>Rebalance pool</h3>
        </div>
        <div className='modal-body'>
            {this.state.output.length > 0 ? <Output message={this.state.output} /> : ''}
        </div>
        <div className='modal-footer'>
            <CancelBtn disabled={this.state.disabled} />
            <Button text="rebalance" disabled={this.state.disabled} onClick={this.rebalance} />
        </div>
      </div>
    )
  }
}
