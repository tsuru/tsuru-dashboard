import React from "react";
import ReactDOM from "react-dom";
import { PoolRebalance } from "../components/pool-rebalance";

var element = document.getElementById('pool-rebalance');
var url = element.dataset.url;

ReactDOM.render(
  <PoolRebalance url={url} />,
  element
);
