import React from "react";
import { shallow } from "enzyme";
import { PoolRebalance } from "../jsx/components/pool-rebalance";

describe('PoolRebalance', () => {
  it('should has pool-rebalance as className', () => {
    const poolRebalance = shallow(<PoolRebalance />);
    expect(poolRebalance.find(".pool-rebalance").length).toBe(1);
  });

  it('initial state', () => {
    const poolRebalance = shallow(<PoolRebalance />);
    expect(poolRebalance.state()).toEqual({disabled: false, output: ''});
  });
});
