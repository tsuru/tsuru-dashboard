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

const controls = document.getElementById('controls');
if (controls) {
  ReactDOM.render(
    <EventFilters
      kind={getParameterByName('kindName')}
      target={getParameterByName('target.value')}
      owner={getParameterByName('ownerName')}
      errorOnly={getParameterByName('errorOnly') === 'true'}
      running={getParameterByName('running') === 'true'}
      includeRemoved={getParameterByName('includeRemoved') === 'true'}
      since={getParameterByName('since')}
      until={getParameterByName('until')}
    />,
    controls
  );
}
