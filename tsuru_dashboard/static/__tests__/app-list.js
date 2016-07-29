import React from "react";
import { shallow, mount } from "enzyme";
import { AppList, AppSearch, AppTable } from "../jsx/components/list";
import { Loading } from "../jsx/components/loading";
import $ from "jquery";

describe('AppList', () => {
  it('should has app-list as className', () => {
    const wrapper = shallow(
      <AppList url="http://localhost:80/apps/list.json" />
    );
    expect(wrapper.find(".app-list").length).toBe(1);
  });

  it ('should be composed by AppSearch and AppTable', () => {
    const wrapper = shallow(
      <AppList url="http://localhost:80/apps/list.json" />
    );
    expect(wrapper.find(".app-list").children().length).toBe(2);
    expect(wrapper.find(AppSearch).length).toBe(1);
    expect(wrapper.find(AppTable).length).toBe(1);
  });

  it ('should contain Loading if its loading', () => {
    const wrapper = shallow(
      <AppList url="http://localhost:80/apps/list.json" />
    );
    wrapper.setState({loading: true})
    expect(wrapper.find(Loading).length).toBe(1);
  });

  it('should load apps on render', () => {
    $.ajax = jest.genMockFunction();
    const wrapper = mount(
      <AppList url="http://localhost:80/apps/list.json" />
    )

    $.ajax.mock.calls[0][0].success({apps: [{name: "appname"}, {name: "otherapp"}]});

    expect({apps: [{name: "appname"}, {name: "otherapp"}], cached: [{name: "appname"}, {name: "otherapp"}], loading: false, term: ''}).toEqual(wrapper.state());

    var items = wrapper.find("td");
    expect(items.length).toBe(2);
  });

  it('should filter list by app name', () => {
    $.ajax = jest.fn((obj) => {
      obj.success({apps: [{name: "appname"}, {name: "other"}]});
    });
    const wrapper = mount(
      <AppList url="http://localhost:80/apps/list.json" />
    )

    wrapper.find("input").simulate('change', {target: {value: "oth"}});
    expect({apps: [{name: "other"}], cached: [{name: "appname"}, {name: "other"}], loading: false, term: ''}).toEqual(wrapper.state());
    expect(wrapper.find("td").length).toBe(1);
  });

  it('should list all on empty search', () => {
    $.ajax = jest.fn((obj) => {
      obj.success({apps: [{name: "appname"}, {name: "other"}]});
    });

    const wrapper = mount(
      <AppList url="http://localhost:80/apps/list.json" />
    )

    wrapper.find("input").simulate('change', {target: {value: ""}});
    expect({apps: [{name: "appname"}, {name: "other"}], cached: [{name: "appname"}, {name: "other"}], loading: false, term: ''}).toEqual(wrapper.state());
	  expect(wrapper.find("td").length).toBe(2);
  });

});
