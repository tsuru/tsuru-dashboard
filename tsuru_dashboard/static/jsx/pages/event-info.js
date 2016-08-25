import React from "react";
import ReactDOM from "react-dom";
import EventCancel from "../components/event-cancel";

$("#cancel-button").on('click', () => {
  ReactDOM.render(
    <EventCancel />,
    document.getElementById('modal')
  );
})
