import React from "react";
import ReactDOM from "react-dom";
import { DeployBox, DeployPopin } from "../components/deploy";

var isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);
var isSafari = /Safari/.test(navigator.userAgent) && /Apple Computer/.test(navigator.vendor);

if (isChrome || isSafari) {
  ReactDOM.render(
    <DeployBox/>,
    document.getElementById('deploy-box')
  );

  ReactDOM.render(
    <DeployPopin/>,
    document.getElementById('deploy')
  );
}
