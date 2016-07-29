import React from "react";
import ReactDOM from "react-dom";
import { Log } from "../components/log";

var url = window.location.pathname + "stream/";
ReactDOM.render(
  <Log url={url} />,
  document.getElementById('logs')
);
