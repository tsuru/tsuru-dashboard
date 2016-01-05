jest.dontMock('../jsx/components/log.jsx');
jest.dontMock('oboe');

var React = require('react'),
    ReactDOM = require('react-dom'),
    Log = require('../jsx/components/log.jsx'),
    TestUtils = require('react-addons-test-utils');

describe('Log', function() {
  it('should has log as classname', function() {
    var log = TestUtils.renderIntoDocument(
      <Log />
    );
  });
});
