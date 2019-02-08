import Cookie from 'js-cookie';
import React, { Component } from "react";
import ReactDOM from "react-dom";

if(typeof window.jQuery === 'undefined') {
    var $ = require('jquery');
} else {
    var $ = window.jQuery;
}

export class AppRemove extends Component {
  constructor(props) {
    super(props);

    this.state = {
      isOnConfirmation: false
    }

    this.onClick = this.onClick.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
  }

  onClick(e) {
    e.preventDefault();
    e.stopPropagation();
    this.setState({isOnConfirmation: !this.state.isOnConfirmation});
  }

  handleCancel(e) {
    this.setState({isOnConfirmation: false});
  }  

  render() {
    return (
      <div className="removeApp">
        <h3>Delete app</h3>
        <div className="content">
          <a className="btn btn-danger" onClick={this.onClick}>Delete app</a>
          {this.state.isOnConfirmation === true ? <AppRemoveConfirmation app={this.props.app}
            onClose={this.handleCancel}/> : ""}
        </div>
      </div>
    )
  }
}

export class AppRemoveConfirmation extends Component {
    constructor(props) {
      super(props);
  
      this.state = {
        confirmation: "",
        isConfirmed: false
      }
  
      this.handleConfirmationChange = this.handleConfirmationChange.bind(this);
      this.handleChange = this.handleChange.bind(this);
      this.handleClose = this.handleClose.bind(this);
      this.appRemove = this.appRemove.bind(this);
    }
  
    componentDidMount() {
      var domElem = $(ReactDOM.findDOMNode(this));
      if(domElem !== undefined){
        domElem.modal('show');
      }
    }
  
    handleConfirmationChange(e) {
      var state = this.state;
      state.confirmation = e.target.value;
      state.isConfirmed = state.confirmation === this.props.app;
      this.setState(state);
    }
  
    handleChange(e) {
      var state = this.state;
      state[e.target.name] = !state[e.target.name];
      this.setState(state);
    }
  
    handleClose(e) {
      e.preventDefault();
      if(this.props.onClose !== undefined) {
        this.props.onClose(e);
      }
    }
  
    appRemove() {
      var app = this.props.app;
      var data = []
      var url = "/apps/"+app+"/remove/"
      
      $.ajax({
        type: "DELETE",
        url: url,
        headers: {
          'X-CSRFToken': Cookie.get('csrftoken')
        },
        data: {},
        success: () => {
          window.location.href = "/apps/"
        },
        error: () => {
          location.reload();
        }
      });
    }
  
    render() {
      return (
        <div id="confirmation" className="modal fade" role="dialog" aria-labelledby="myModalLabel">
        <div className="modal-dialog" role="document">
          <div className="modal-content">
            <div className="modal-header">
              <button type="button" className="close" data-dismiss="modal" aria-hidden="true" onClick={this.handleClose}>×</button>
              <h3 id="myModalLabel">Are you sure?</h3>
            </div>
            <div className="modal-body">
              <p>This action <strong>CANNOT</strong> be undone. This will permanently delete the <strong>{this.props.app}</strong> application.</p>
              <p>Please type in the name of your application to confirm.</p>
              <input type="text" className="remove-confirmation" value={this.state.confirmation} onChange={this.handleConfirmationChange} />
            </div>
            <div className="modal-footer">
                <button className="btn cancel" data-dismiss="modal" aria-hidden="true" onClick={this.handleClose}>Cancel</button>
                <button className="btn btn-danger btn-remove" onClick={this.appRemove} disabled={!this.state.isConfirmed}>I understand the consequences, delete this application</button>
            </div>
          </div>
        </div>
      </div>
      )
    }
}


export class AppUnlockConfirmation extends Component {
  constructor(props) {
    super(props);

    this.state = {
      confirmation: "",
      isConfirmed: false
    }

    this.handleConfirmationChange = this.handleConfirmationChange.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleClose = this.handleClose.bind(this);
    this.appUnlock = this.appUnlock.bind(this);
  }

  componentDidMount() {
    var domElem = $(ReactDOM.findDOMNode(this));
    if(domElem !== undefined){
      domElem.modal('show');
    }
  }

  handleConfirmationChange(e) {
    var state = this.state;
    state.confirmation = e.target.value;
    state.isConfirmed = state.confirmation === this.props.app;
    this.setState(state);
  }

  handleChange(e) {
    var state = this.state;
    state[e.target.name] = !state[e.target.name];
    this.setState(state);
  }

  handleClose(e) {
    e.preventDefault();
    if(this.props.onClose !== undefined) {
      this.props.onClose(e);
    }
  }

  appUnlock() {
    var app = this.props.app;
    var data = []
    var url = "/apps/"+app+"/unlock/"
    
    $.ajax({
      type: "POST",
      url: url,
      headers: {
        'X-CSRFToken': Cookie.get('csrftoken')
      },
      data: {},
      success: () => {
        window.location.href = "/apps/"+app+"/settings/"
      },
      error: () => {
        location.reload();
      }
    });
  }

  render() {
    return (
      <div className="modal-dialog" role="document">
        <div className="modal-content">
          <div className="modal-header">
            <button type="button" className="close" data-dismiss="modal" aria-hidden="true" onClick={this.handleClose}>×</button>
            <h3 id="myModalLabel">Unlock { this.props.app }</h3>
          </div>
          <div className="modal-body">
            <p>Please type in the name of your application to confirm.</p>
            <input type="text" className="unlock-confirmation" value={this.state.confirmation} onChange={this.handleConfirmationChange} />
          </div>
          <div className="modal-footer">
              <button className="btn cancel" data-dismiss="modal" aria-hidden="true" onClick={this.handleClose}>Cancel</button>
              <button className="btn btn-unlock" onClick={this.appUnlock} disabled={!this.state.isConfirmed}>Unlock app</button>
          </div>
        </div>
      </div>
    )
  }
}

