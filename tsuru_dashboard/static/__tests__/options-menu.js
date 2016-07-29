import React from "react";
import { shallow, mount } from "enzyme";
import { OptionsMenu } from "../jsx/components/options-menu";

describe('OptionMenu', () => {
  it('has options-menu as className', () => {
    const optionsMenu = shallow(<OptionsMenu />);
    expect(optionsMenu.find(".options-menu").length).toBe(1);
  });

  it('contains options items', () => {
    const optionsMenu = mount(
      <OptionsMenu items={["about", "docs"]} />
    );
    expect(optionsMenu.find('.options-item').length).toBe(2);
  });
});
