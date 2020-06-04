import React from "react";
import ReactDOM from "react-dom";
import { NodeCreate } from "../components/node-create";

var pool = window.location.pathname.split("/")[3];

ReactDOM.render(
  <NodeCreate pool={pool} />,
  document.getElementById('node-create')
);
