import React from "react";
import ReactDOM from "react-dom";
import { EventFilters } from "../components/event-list";

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return '';
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

ReactDOM.render(
  <EventFilters
    kind={getParameterByName('kindName')}
    errorOnly={getParameterByName('errorOnly') === 'true'}
    running={getParameterByName('running') === 'true'}
  />,
  document.getElementById('controls')
);
