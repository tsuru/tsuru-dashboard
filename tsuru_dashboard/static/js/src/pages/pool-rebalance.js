import React from "react";
import ReactDOM from "react-dom";
import { PoolRebalance } from "../components/pool-rebalance";

var element = document.getElementById('pool-rebalance');
var url = element.dataset.url;
var poolName = element.dataset.poolname;

ReactDOM.render(
  <PoolRebalance url={url} poolName={poolName} />,
  element
);
