import React from "react";
import { shallow } from "enzyme";
import { Log } from "../js/src/components/log";

describe('Log', () => {
  it('should has log as classname', () => {
    var wrapper = shallow(<Log url="http://localhost/log"/>);
    wrapper.setState({logging: true});
    expect(wrapper.children().find(".log").length).toBe(1);
  });
});
