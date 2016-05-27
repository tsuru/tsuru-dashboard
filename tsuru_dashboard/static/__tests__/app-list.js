jest.dontMock('../jsx/components/list.jsx');
jest.dontMock('fuzzy');

var React = require('react'),
    Enzyme = require('enzyme'),
    List = require('../jsx/components/list.jsx'),
    AppList = List.AppList,
    AppSearch = List.AppSearch,
    AppTable = List.AppTable,
    Loading = require('../jsx/components/loading.jsx'),
    $ = require('jquery');

describe('AppList', function() {
  it('should has app-list as className', function() {
    const wrapper = Enzyme.shallow(
      <AppList url="http://localhost:80/apps/list.json" />
    );
    expect(wrapper.find(".app-list").length).toBe(1);
  });

  it ('should be composed by AppSearch and AppTable', function() {
    const wrapper = Enzyme.shallow(
      <AppList url="http://localhost:80/apps/list.json" />
    );
    expect(wrapper.find(".app-list").children().length).toBe(2);
    expect(wrapper.find(AppSearch).length).toBe(1);
    expect(wrapper.find(AppTable).length).toBe(1);
  });

  it ('should contain Loading if its loading', function() {
    const wrapper = Enzyme.shallow(
      <AppList url="http://localhost:80/apps/list.json" />
    );
    wrapper.setState({loading: true})
    expect(wrapper.find(Loading).length).toBe(1);
  });

  it('should load apps on render', function() {
    const wrapper = Enzyme.mount(
      <AppList url="http://localhost:80/apps/list.json" />
    )

    $.ajax.mock.calls[0][0].success({apps: [{name: "appname"}, {name: "otherapp"}]});

    expect({apps: [{name: "appname"}, {name: "otherapp"}], cached: [{name: "appname"}, {name: "otherapp"}], loading: false, term: ''}).toEqual(wrapper.state());

    var items = wrapper.find("td");
    expect(items.length).toBe(2);
  });

  it('should filter list by app name', function() {
    const wrapper = Enzyme.mount(
      <AppList url="http://localhost:80/apps/list.json" />
    )

    $.ajax.mock.calls[1][0].success({apps: [{name: "appname"}, {name: "other"}]});

    wrapper.find("input").simulate('change', {target: {value: "oth"}});
    expect({apps: [{name: "other"}], cached: [{name: "appname"}, {name: "other"}], loading: false, term: ''}).toEqual(wrapper.state());
    expect(wrapper.find("td").length).toBe(1);
  });

  it('should list all on empty search', function() {
    const wrapper = Enzyme.mount(
      <AppList url="http://localhost:80/apps/list.json" />
    )

    $.ajax.mock.calls[2][0].success({apps: [{name: "appname"}, {name: "other"}]});

    wrapper.find("input").simulate('change', {target: {value: ""}});
    expect({apps: [{name: "appname"}, {name: "other"}], cached: [{name: "appname"}, {name: "other"}], loading: false, term: ''}).toEqual(wrapper.state());
	  expect(wrapper.find("td").length).toBe(2);
  });

});
