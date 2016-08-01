import React from "react";
import { shallow, mount } from "enzyme";
import { KindSelect } from "../jsx/components/event-list";

describe('KindSelect', () => {
  it('initial state', () => {
    const select = mount(<KindSelect />);
    expect(select.find("option").length).toBe(1);
  });
});
