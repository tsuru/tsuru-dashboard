import React from "react";
import { shallow, mount } from "enzyme";
import EventCancel from "../jsx/components/event-cancel";
import Modal from "backstage-modal";

describe('<EventCancel />', () => {
  it('initial state', () => {
    const cancel = shallow(<EventCancel />);
    const modal = cancel.find(Modal);
    expect(modal.length).toBe(1);
  });

  it('cancel button disabled by default', () => {
    const cancel = shallow(<EventCancel />);
    const button = cancel.find('button');
    expect(button.prop('disabled')).toBe(true);
  });
});
