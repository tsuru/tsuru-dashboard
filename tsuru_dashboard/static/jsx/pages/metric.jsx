var React = require('react'),
    ReactDOM = require('react-dom'),
    GraphContainer = require("../components/metrics.jsx").GraphContainer;

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
$("select[name=serie]").val(queryString("serie"));
$("input[name=kind]").val(queryString("kind"));

var kind = queryString("kind");
var interval = queryString("serie");
var from = queryString("from");

var titles = {
  "cpu_max": "cpu (%)",
  "mem_max": "memory (MB)",
  "swap": "swap (MB)",
  "requests_min": "requests min",
  "response_time": "response time (seconds)",
  "http_methods": "http methods",
  "status_code": "status code",
  "nettx": "net up (KB/s)",
  "netrx": "net down (KB/s)"
};

ReactDOM.render(
  <div className="metrics">
    <GraphContainer kind={kind} title={titles[kind]? titles[kind] : kind} appName={appName} interval={interval} from={from} legend={true} />
  </div>,
  document.getElementById('metrics')
);
