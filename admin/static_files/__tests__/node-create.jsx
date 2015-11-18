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

  it('should initial state', function() {
    var nodeCreate = TestUtils.renderIntoDocument(
      <NodeCreate />
    );
  
    expect(nodeCreate.state.templates.length).toBe(0);
    expect(nodeCreate.state.metadata.length).toBe(0);
    expect(nodeCreate.state.register).toBeFalsy();
  });
});

