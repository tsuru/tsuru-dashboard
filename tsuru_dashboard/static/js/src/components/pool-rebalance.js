import React, { Component } from "react";
import { Button, Output, CancelBtn } from "./base";

if (typeof window.jQuery === 'undefined') {
  var $ = require('jquery');
} else {
  var $ = window.jQuery;
}

class PoolRebalanceConfirmation extends Component {
  constructor(props) {
    super(props);

    this.state = {
      value: "",
      ok: false
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleStart = this.handleStart.bind(this);
  }

  handleChange(event) {
    if (event.target.value === this.props.poolName) {
      this.setState({value: event.target.value, ok: true});
    } else {
      this.setState({value: event.target.value});
    }
  }

  handleStart() {
    this.props.startRebalance();
  }

  render() {
    return (
      <div className="modal-dialog" role="document">
        <div className="modal-content">
          <div className="modal-header">
            <button type="button" className="close" dataDismiss="modal" ariaHidden="true">×</button>
            <h3 id="myModalLabel">Are you sure?</h3>
          </div>
          <div className="modal-body">
            <p>This action <strong>CANNOT</strong> be undone. This will permanently rebalance the <strong>{this.props.poolName}</strong> pool.</p>
            <p>Please type in the pool name to confirm.</p>
            <input type="text" className="rebalance-confirmation" value={this.state.value} onChange={this.handleChange} />
          </div>
          <div className="modal-footer">
            <button className="btn" dataDismiss="modal" ariaHidden="true">Cancel</button>
            <button className="btn btn-danger btn-rebalance" disabled={this.state.ok ? "" : "disabled"} onClick={this.handleStart}>I understand the consequences, rebalance this pool</button>
          </div>
        </div>
      </div>
    )
  }
}

export class PoolRebalance extends Component {
  constructor(props) {
    super(props);

    this.state = {
      output: "",
      disabled: false,
      confirmed: false
    }

    this.rebalance = this.rebalance.bind(this);
    this.startRebalance = this.startRebalance.bind(this);
  }

  rebalance() {
    this.setState({disabled: true, output: 'Wait until rebalance is started.'});
    var xhr = new XMLHttpRequest();
    xhr.open('POST', this.props.url, true);
    xhr.onprogress = () => {
      this.setState({output: xhr.responseText});
    };
    var self = this;
    xhr.onload = () => {
      self.setState({disabled: false});
    };
    xhr.send();
  }

  startRebalance() {
    var self = this;
    this.setState({confirmed: true}, function() {
      self.rebalance();
    });
  }

  render() {
    if (!this.state.confirmed) {
      return <PoolRebalanceConfirmation poolName={this.props.poolName} startRebalance={this.startRebalance} />;
    }

    return (
      <div className="modal-dialog" role="document">
        <div className="modal-content">
          <div className="modal-header">
              <h3 id="myModalLabel">Rebalance pool</h3>
          </div>
          <div className="modal-body">
              {this.state.output.length > 0 ? <Output message={this.state.output} /> : ""}
          </div>
          <div className="modal-footer">
              <CancelBtn disabled={this.state.disabled} />
              <Button text="rebalance" disabled={this.state.disabled} onClick={this.rebalance} />
          </div>
        </div>
      </div>
    )
  }
}
