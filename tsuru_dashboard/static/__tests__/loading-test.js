import React from "react";
import { shallow } from "enzyme";
import { Loading } from "../jsx/components/loading";

describe('Loading', () => {
  it('renders an element with "loader" class', () => {
    var wrapper = shallow(<Loading />);
    expect(wrapper.find(".loader").length).toBe(1);
  });
});
