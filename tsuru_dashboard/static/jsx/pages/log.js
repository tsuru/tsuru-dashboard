import React from "react";
import ReactDOM from "react-dom";
import { Log } from "../components/log";

function getParameterByName(name) {
    url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return '';
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

var url = window.location.pathname + "stream/";
var appInfoUrl = "/apps/" + window.location.pathname.split("/")[2] + ".json";
ReactDOM.render(
  <Log url={url}
    source={getParameterByName("source")}
    unit={getParameterByName("unit")}
    appInfoUrl={appInfoUrl}
  />,
  document.getElementById('log')
);
