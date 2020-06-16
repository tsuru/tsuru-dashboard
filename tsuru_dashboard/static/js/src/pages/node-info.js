import React from "react";
import ReactDOM from "react-dom";
import { NodeInfo } from "../components/node-info";

const settingsElem = document.getElementById('django-settings');
let settings = {};
if (settingsElem) {
    settings = JSON.parse(settingsElem.textContent);
}

var url = window.location.pathname + "containers";
ReactDOM.render(
  <NodeInfo url={url} settings={settings}/>,
  document.getElementById('node-info')
);
