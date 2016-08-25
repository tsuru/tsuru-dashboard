import React, { Component } from 'react';
import Modal from "backstage-modal";

export default class EventCancel extends Component {
  constructor(props) {
    super(props);

    this.cancel = this.cancel.bind(this);
  }

  cancel() {
    $.ajax({
      type: 'POST',
      url: "/events/" + this.props.uuid + "/cancel/",
      data: {reason: this.refs.reason.value},
      success: () => {
        window.location = "/events/";
      }
    });
  }

  render() {
    return (
      <Modal title="cancel event" isOpen>
        <div>
          <p>This action CANNOT be undone.
          This will cancel this event.</p>

          <p>Type the reason here to continue:</p>
          <p><input type="text" ref="reason" /></p>
        </div>
        <div>
          <button className="button" onClick={this.cancel}>
            cancel
          </button>
        </div>
      </Modal>
    );
  }
}
