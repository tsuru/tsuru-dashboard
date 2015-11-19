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
    expect(nodeCreate.state.metadata).toEqual({});
    expect(nodeCreate.state.register).toBeFalsy();
  });

  it('change register state on click', function() {
    var nodeCreate = TestUtils.renderIntoDocument(
      <NodeCreate />
    );
    var register = TestUtils.findRenderedDOMComponentWithClass(nodeCreate, "register");

    expect(nodeCreate.state.register).toBeFalsy();
    expect(nodeCreate.state.metadata).toEqual({});

    TestUtils.Simulate.click(register);
    expect(nodeCreate.state.register).toBeTruthy();
    expect(nodeCreate.state.metadata).toEqual({"address": ""});

    TestUtils.Simulate.click(register);
    expect(nodeCreate.state.register).toBeFalsy();
    expect(nodeCreate.state.metadata).toEqual({});
  });

  it('don"t show template select on empty templates', function() {
    var nodeCreate = TestUtils.renderIntoDocument(
      <NodeCreate />
    );
    var templates = TestUtils.scryRenderedDOMComponentsWithClass(nodeCreate, "template");

    expect(templates.length).toBe(0);
  });

  it('metadata items', function() {
    var nodeCreate = TestUtils.renderIntoDocument(
      <NodeCreate />
    );
    nodeCreate.addMetadata("key", "value");
    nodeCreate.addMetadata("anotherkey", "v");
    var items = TestUtils.scryRenderedDOMComponentsWithClass(nodeCreate, "meta-item");

    expect(items.length).toEqual(3);

    var item = ReactDOM.findDOMNode(items[0]);
    var key = item.childNodes[0].childNodes[1];
    expect(key.attributes["value"].value).toEqual("key");
    var value = item.childNodes[1].childNodes[1];
    expect(value.attributes["value"].value).toEqual("value");

    var item = ReactDOM.findDOMNode(items[1]);
    var key = item.childNodes[0].childNodes[1];
    expect(key.attributes["value"].value).toEqual("anotherkey");
    var value = item.childNodes[1].childNodes[1];
    expect(value.attributes["value"].value).toEqual("v");

    var item = ReactDOM.findDOMNode(items[2]);
    var key = item.childNodes[0].childNodes[1];
    expect(key.attributes["value"].value).toEqual("");
    var value = item.childNodes[1].childNodes[1];
    expect(value.attributes["value"].value).toEqual("");
  });

});

