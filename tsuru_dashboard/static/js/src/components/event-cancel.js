import Cookie from 'js-cookie';
import React, { Component } from 'react';
import Modal from "backstage-modal";

export default class EventCancel extends Component {
  constructor(props) {
    super(props);

    this.cancel = this.cancel.bind(this);
    this.onChange = this.onChange.bind(this);

    this.state = { enabled: false };
  }

  cancel() {
    $.ajax({
      type: 'POST',
      url: `/events/${this.props.uuid}/cancel/`,
      headers: {
        'X-CSRFToken': Cookie.get('csrftoken'),
      },
      data: {reason: this.refs.reason.value},
      success: () => {
        window.location = "/events/";
      }
    });
  }

  onChange() {
    this.setState({ enabled: this.refs.reason.value.length > 0 });
  }

  render() {
    return (
      <Modal title="cancel event" isOpen>
        <div>
          <p>This action CANNOT be undone.
          This will cancel this event.</p>

          <p>Type the reason here to continue:</p>
          <p>
            <input type="text" ref="reason" onChange={this.onChange} />
          </p>
        </div>
        <div>
          <button
            className="button"
            onClick={this.cancel}
            disabled={!this.state.enabled}
          >
            cancel
          </button>
        </div>
      </Modal>
    );
  }
}
