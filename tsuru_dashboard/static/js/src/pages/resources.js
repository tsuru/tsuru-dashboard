import React from "react";
import ReactDOM from "react-dom";
import { Resources } from "../components/resources";

var url = "/apps/" + window.location.pathname.split("/")[2] + ".json";
ReactDOM.render(
  <Resources url={url} />,
  document.getElementById('resources')
);
