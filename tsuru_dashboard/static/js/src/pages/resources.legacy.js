import React from "react";
import ReactDOM from "react-dom";
import { Resources } from "../components/resources.legacy";

var url = "/apps/" + window.location.pathname.split("/")[2] + ".json";
var settings = JSON.parse(document.getElementById("settings").textContent);
var resources = document.getElementById("resources");

if (settings.GRAFANA_URL) {
  const req = new Request(settings.GRAFANA_URL, { mode: "no-cors" });
  fetch(req)
    .then(function () {
      ReactDOM.render(
        <iframe className="grafana_frame" src={settings.GRAFANA_URL} />,
        resources
      );
    })
    .catch(function (err) {
      console.info(
        "Failed to load grafana metrics, fallback to legacy backend",
        err
      );
      ReactDOM.render(
        <Resources url={url} settings={settings} />,
        resources
      );
    });
} else {
  ReactDOM.render(
    <Resources url={url} settings={settings} />,
    resources
  );
}
