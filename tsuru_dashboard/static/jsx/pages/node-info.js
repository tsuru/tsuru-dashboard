import React from "react";
import ReactDOM from "react-dom";
import { NodeInfo } from "../components/node-info";

var url = window.location.pathname + "containers";
ReactDOM.render(
  <NodeInfo url={url} />,
  document.getElementById('node-info')
);
