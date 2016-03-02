var React = require('react'),
    ReactDOM = require('react-dom'),
    TopSlow = require("../components/top-slow.jsx").TopSlow;

var appName = window.location.pathname.split("/")[2];

var queryString = function(key) {
  var keys = {};
  var items = window.location.search.substr(1).split("&");
  $.each(items, function(i, item) {
    var keyValue = item.split("=");
    keys[keyValue[0]] = keyValue[1];
  });
  return keys[key];
}

$("select[name=from]").val(queryString("from"));
$("select[name=kind]").val(queryString("kind"));

var from = queryString("from");
var kind = queryString("kind");

if(kind == "response_time"){
  ReactDOM.render(
    <div className="metrics">
      <TopSlow kind={"top_slow"} appName={appName} from={from}/>
    </div>,
    document.getElementById('top-slow')
  );
}
