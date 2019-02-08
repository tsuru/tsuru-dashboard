import React from "react";
import ReactDOM from "react-dom";
import { AppRemove, AppUnlockConfirmation } from "../components/app-settings";

var app = window.location.pathname.split("/")[2];
ReactDOM.render(
  <AppRemove app={app} />,
  document.getElementById('app-remove')
);

$(".unlock").on('click', function(ev) {
  ev.preventDefault();
  ReactDOM.render(
    <AppUnlockConfirmation app={app} />,
    document.getElementById('unlock')
  );
});