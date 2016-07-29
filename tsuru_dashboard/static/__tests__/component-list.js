import React from "react";
import { mount, shallow } from "enzyme";
import $ from "jquery";
import { Component, ComponentList } from "../jsx/components/component-list";
import { Metrics } from "../jsx/components/metrics";

describe('ComponentList', () => {
  it('fetches the components url', () => {
    var ajax = $.ajax;
    $.ajax = jest.genMockFunction();
    const componentList = mount(
      <ComponentList url={"components.json"}/>
    );

    expect($.ajax.mock.calls.length).toBe(1);
    expect($.ajax.mock.calls[0][0].url).toBe("components.json");
    $.ajax = ajax;
  });

  it('has component-list as classname', () => {
    const componentList = shallow(<ComponentList />);

    expect(componentList.find(".component-list").length).toBe(1);
  });

  it('renders a component for each one that was fetched', () => {
    $.getJSON= jest.genMockFunction();
    var ajax = $.ajax;
    $.ajax = jest.fn((obj) => {
      obj.success({components: ["registry", "big-sibling"]});
    });
    const componentList = mount(<ComponentList />);
    var components = componentList.find(Component);

    expect(components.length).toBe(2);
    expect(components.first().props().name).toBe("registry");
    expect(components.last().props().name).toBe("big-sibling");
    $.ajax = ajax;
  });
});

describe('Component', () => {
  it('renders Metrics for the component', () => {
    var ajax = $.ajax;
    $.ajax = jest.genMockFunction();
    const component = mount(
      <Component name={"big-sibling"}/>
    );
    var metrics = component.find(Metrics);

    expect(metrics.length).toBe(1);
    expect(metrics.props().targetName).toBe("big-sibling");
    expect(metrics.props().targetType).toBe("component");
    $.ajax = ajax;
  });

  it('has component as classname', () => {
    const component = shallow(<Component />);

    expect(component.find(".component").length).toBe(1);
  });
});
