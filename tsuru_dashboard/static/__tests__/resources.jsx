jest.dontMock('../jsx/components/resources.jsx');

var React = require('react'),
    ReactDOM = require('react-dom'),
    Resources = require('../jsx/components/resources.jsx'),
    TestUtils = require('react-addons-test-utils');

describe('Resources', function() {
  it('should has resources as className', function() {
    var list = TestUtils.renderIntoDocument(
      <Resources />
    );
    
    expect(ReactDOM.findDOMNode(list).className).toEqual("resources");
  });
});
