import React from "react";
import ReactDOM from "react-dom";
import { AppList } from "../components/list";

ReactDOM.render(
  <AppList url="/apps/list.json" />,
  document.getElementById('list-container')
);
