import React from "react";
import ReactDOM from "react-dom";
import EventCancel from "../components/event-cancel";

$("#cancel-button").on('click', () => {
  ReactDOM.render(
    <EventCancel uuid={window.location.pathname.split('/')[2]} />,
    document.getElementById('modal')
  );
});
