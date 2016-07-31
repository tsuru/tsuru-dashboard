import React from "react";
import { shallow, mount } from "enzyme";
import { Tab, Tabs, Select } from "../jsx/components/base";

describe('Tabs', () => {
  it('should render a tab with correct name', () => {
    const tabs = shallow(<Tabs tabs={["tab1"]}/>);
    var tab = tabs.find(Tab);
    expect(tab.props().name).toBe("tab1");
  });

  it('should render a Tab for each element', () => {
    const tabs = shallow(<Tabs tabs={["tab1", "tab2"]}/>);
    expect(tabs.find(Tab).length).toBe(2);
  });
});

describe('Tab', () => {
  it('has no className if its not active', () => {
    const tab = shallow(<Tab name={"tab"} active={false} />);
    expect(tab.find(".active").length).toBe(0);
  });

  it('has className active if its active', () => {
    const tab = shallow(<Tab name={"tab"} active={true} />);
    expect(tab.find(".active").length).toBe(1);
  });

  it('triggers setActive on click', () => {
    var setActive = jest.genMockFunction();
    const tab = mount(<Tab name={"tab"} active={false} setActive={setActive}/>);
    expect(setActive.mock.calls.length).toBe(0);
    tab.find("a").simulate("click");
    expect(setActive.mock.calls.length).toBe(1);
  });
});

describe('Select', () => {
  it('initial state', () => {
    const select = shallow(<Select />);
    expect(select.find("option").length).toBe(0);
  });

  it('suport custom options', () => {
    const select = shallow(<Select options={["one", "two"]} />);
    expect(select.find("option").length).toBe(2);
  });

  it('default option', () => {
    const select = shallow(<Select defaultOption="ble" options={[]} />);
    expect(select.find("option").text()).toBe("ble");
    expect(select.find("option").length).toBe(1);
  });
});
