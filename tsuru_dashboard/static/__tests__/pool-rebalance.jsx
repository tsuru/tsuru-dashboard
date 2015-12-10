jest.dontMock('../jsx/components/base.jsx');
jest.dontMock('../jsx/components/pool-rebalance.jsx');

var React = require('react'),
    ReactDOM = require('react-dom'),
    base = require('../jsx/components/base.jsx'),
    PoolRebalance = require('../jsx/components/pool-rebalance.jsx'),
    TestUtils = require('react-addons-test-utils');

describe('PoolRebalance', function() {
  it('should has pool-rebalance as className', function() {
    var poolRebalance = TestUtils.renderIntoDocument(
      <PoolRebalance />
    );

    expect(ReactDOM.findDOMNode(poolRebalance).className).toEqual("pool-rebalance");
  });

  it('initial state', function() {
    var poolRebalance = TestUtils.renderIntoDocument(
      <PoolRebalance />
    );

    expect(poolRebalance.state).toEqual({disabled: false, output: ''});
  });
});
