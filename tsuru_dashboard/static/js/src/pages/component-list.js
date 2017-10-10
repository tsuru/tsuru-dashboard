import React from "react";
import ReactDOM from "react-dom";
import { ComponentList } from "../components/component-list";

ReactDOM.render(
  <ComponentList url="/components/list.json" />,
  document.getElementById('list-container')
);
