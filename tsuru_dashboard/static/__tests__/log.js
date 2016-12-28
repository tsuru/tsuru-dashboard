import React from "react";
import { mount } from "enzyme";
import { Log } from "../jsx/components/log";

describe('Log', () => {
  it('should has log as classname', () => {
    var wrapper = mount(<Log url="http://localhost/log"/>);
    wrapper.setState({logging: true});
    expect(wrapper.children().find(".log").length).toBe(1);
  });
});
