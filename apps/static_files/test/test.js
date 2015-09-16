var assert = require("chai").assert,
    React = require("react"),
    TestUtils = require("react/addons").addons.TestUtils,
    List = require("../jsx/components/list.jsx");

describe('AppSearch', function() {
  before(function() {
    if(!global.document){
      global.document = require('jsdom').jsdom();
      global.window = document.parentWindow;
    }
    this.executed = false;
    var that = this;
    var onSearch = function() { that.executed = true; }
    this.appSearch = TestUtils.renderIntoDocument(
      React.createElement(List.AppSearch, {onSearchSubmit: onSearch})
    );
  });

  it('should has search as className', function () {
    assert.equal('search', this.appSearch.getDOMNode().getAttribute('class'));
  });

  it('should execute onSearchSubmit on change', function () {
    var form = TestUtils.findRenderedDOMComponentWithTag(this.appSearch, 'form');
    TestUtils.Simulate.change(form, {target: {value: 'a'}});
    assert.equal(this.executed, true);
  });
});

describe('App', function() {
  before(function() {
    if(!global.document){
      global.document = require('jsdom').jsdom();
      global.window = document.parentWindow;
    }
    this.app = TestUtils.renderIntoDocument(
      React.createElement(List.App, {name: "app-name"})
    );
  });

  it('should has injectable href', function () {
    var a = TestUtils.findRenderedDOMComponentWithTag(this.app, 'a');
    assert.equal('app-name', a.getDOMNode().getAttribute('href'));
  });
});

describe('AppTable', function() {
  before(function() {
    var shallowRenderer = TestUtils.createRenderer();
    var data = {apps: [{name: "app-name"}]}
    shallowRenderer.render(React.createElement(List.AppTable, {data: data}));
    this.table = shallowRenderer.getRenderOutput();
  });

  it('should be composed by a list of apps', function () {
    var apps = this.table.props.children.filter(function(component) {
      return TestUtils.isElementOfType(component, List.App);
    });
    assert.equal(1, apps.length);
  });
});
