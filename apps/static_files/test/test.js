var assert = require("chai").assert,
    React = require("react"),
    TestUtils = require("react/addons").addons.TestUtils,
    FakeXMLHttpRequest = require('fakexmlhttprequest');

var requests = [];

global.XMLHttpRequest = function() {
    var r =  new FakeXMLHttpRequest(arguments)
    requests.push(r)
    return r
}

var List = require("../jsx/components/list.jsx"),
    Loading = require("../jsx/components/loading.jsx");

describe('AppSearch', function() {
  before(function() {
    if(!global.document){
      global.document = require('jsdom').jsdom();
      global.window = document.parentWindow;
    }
    this.executed = false;
    var onSearch = function() { this.executed = true; }.bind(this);
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
    var shallowRenderer = TestUtils.createRenderer();
    var data = {apps: [{name: "app-name"}]}
    shallowRenderer.render(React.createElement(List.App, {name: "app-name"}));
    this.app = shallowRenderer.getRenderOutput();
  });

  it('should has injectable href', function () {
    var td = this.app.props.children;
    var a = td.props.children;
    assert.equal('app-name', a.props.href);
  });
});

describe('AppTable', function() {
  before(function() {
    var shallowRenderer = TestUtils.createRenderer();
    var data = [{name: "app-name"}];
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

describe('AppList', function() {
  it('should has app-list as className', function () {
    var shallowRenderer = TestUtils.createRenderer();
    var data = {apps: [{name: "app-name"}]}
    shallowRenderer.render(React.createElement(List.AppList, {url: "/app/list.json"}));
    var list = shallowRenderer.getRenderOutput();
    assert.equal('app-list', list.props.className);
  });

  it('should be composed by AppSearch, Loading and AppTable', function () {
    var shallowRenderer = TestUtils.createRenderer();
    var data = {apps: [{name: "app-name"}]}
    shallowRenderer.render(React.createElement(List.AppList, {url: "/app/list.json"}));
    var list = shallowRenderer.getRenderOutput();

    assert.lengthOf(list.props.children, 3);

    var appSearch = list.props.children[0];
    assert.isTrue(TestUtils.isElementOfType(appSearch, List.AppSearch));

    var loading = list.props.children[1];
    assert.equal(loading, '');

    var appTable = list.props.children[2];
    var initialState = {data: []};
    assert.deepEqual(initialState, appTable.props);
    assert.isTrue(TestUtils.isElementOfType(appTable, List.AppTable));
  });
});
