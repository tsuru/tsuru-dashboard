import React from "react";
import ReactDOM from "react-dom";
import { DeployBox, DeployPopin, RollbackPopin } from "../components/deploy";

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

var app = window.location.pathname.split("/")[2]

$(".rollback").on('click', function(ev) {
  ev.preventDefault();
  var rollbackUrl = $(this).attr("rollback-url");
  ReactDOM.render(
      <RollbackPopin app={app} url={rollbackUrl}/>,
      document.getElementById('rollback')
  );
});
