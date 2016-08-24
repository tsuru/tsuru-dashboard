import React from "react";
import ReactDOM from "react-dom";
import Modal from "backstage-modal";

$("#cancel-button").on('click', () => {
ReactDOM.render(
  <Modal title="cancel event" isOpen>
    <div>
      <p>This action CANNOT be undone.
      This will cancel this event.</p>

      <p>Type the reason here to continue:</p>
      <p><input type="text" /></p>
    </div>
    <div>
      <button className="button">cancel</button>
    </div>
  </Modal>,
  document.getElementById('modal')
);
})
