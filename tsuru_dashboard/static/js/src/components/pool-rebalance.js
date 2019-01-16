import Cookie from 'js-cookie';
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
  }

  handleChange(event) {
    var newState = {value: event.target.value};
    if (event.target.value === this.props.poolName) {
      newState.ok = true;
    }
    this.setState(newState);
  }

  render() {
    return (
      <div className="modal-dialog">
        <div className="modal-content">
          <div className="modal-header">
            <h3 id="myModalLabel">Are you sure?</h3>
          </div>
          <div className="modal-body">
            <p>This action <strong>CANNOT</strong> be undone. This will permanently rebalance the <strong>{this.props.poolName}</strong> pool.</p>
            <p>Please type in the pool name to confirm.</p>
            <input type="text" className="rebalance-confirmation" value={this.state.value} onChange={this.handleChange} />
          </div>
          <div className="modal-footer">
            <button className="btn" onClick={this.props.onClose}>Cancel</button>
            <button className="btn btn-danger btn-rebalance" disabled={this.state.ok ? "" : "disabled"} onClick={this.props.onStart}>I understand the consequences, rebalance this pool</button>
          </div>
        </div>
      </div>
    )
  }
}

PoolRebalanceConfirmation.defaultProps = {
  onStart: () => {},
  onClose: () => {}
};

export class PoolRebalance extends Component {
  constructor(props) {
    super(props);

    this.state = {
      output: "",
      running: false,
      confirmed: false
    }

    this.rebalance = this.rebalance.bind(this);
    this.startRebalance = this.startRebalance.bind(this);
    this.handleClose = this.handleClose.bind(this);
  }

  rebalance() {
    this.setState({running: true, output: "Wait until rebalance is started."});
    var self = this;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", this.props.url, true);
    xhr.setRequestHeader('X-CSRFToken', Cookie.get('csrftoken'));
    xhr.onprogress = () => {
      this.setState({output: xhr.responseText}, () => {
        self.refs.modalBody.scrollTop += 200;
      });
    };
    xhr.onload = () => {
      self.setState({running: false});
    };
    xhr.send();
  }

  startRebalance() {
    var self = this;
    this.setState({confirmed: true}, function() {
      self.rebalance();
    });
  }

  hide() {
    $("#pool-rebalance").modal("hide");
  }

  handleClose() {
    this.hide();
    this.setState({running: false, confirmed: false, output: ""});
  }

  render() {
    if (!this.state.confirmed) {
      return (
        <PoolRebalanceConfirmation
          poolName={this.props.poolName}
          onStart={this.startRebalance}
          onClose={this.hide} />
      );
    }

    return (
      <div className="modal-dialog pool-rebalance-output">
        <div className="modal-content">
          <div className="modal-header">
            <h3 id="myModalLabel">Rebalance pool</h3>
          </div>
          <div className="modal-body" ref="modalBody">
            {this.state.output.length > 0 ? <Output message={this.state.output} /> : ""}
          </div>
          <div className="modal-footer">
            <Button disabled={this.state.running ? "disabled" : ""} text="Close" onClick={this.handleClose} />
          </div>
        </div>
      </div>
    )
  }
}
