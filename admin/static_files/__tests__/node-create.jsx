jest.dontMock('../jsx/components/node-create.jsx');

var React = require('react'),
    ReactDOM = require('react-dom'),
    NodeCreate = require('../jsx/components/node-create.jsx'),
    TestUtils = require('react-addons-test-utils');

describe('NodeCreate', function() {
  it('should has node-create as className', function() {
    var nodeCreate = TestUtils.renderIntoDocument(
      <NodeCreate />
    );
    
    expect(ReactDOM.findDOMNode(nodeCreate).className).toEqual("node-create");
  });
});
