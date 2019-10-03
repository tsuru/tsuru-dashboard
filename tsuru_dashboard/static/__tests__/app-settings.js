import React from "react";
import { shallow, mount } from "enzyme";
import $ from "jquery";
import { AppRemove, AppRemoveConfirmation, AppUnlockConfirmation } from "../js/src/components/app-settings";


describe('AppRemove', () => {
  var fakeEvent = { preventDefault() {}, stopPropagation() {} };
  it('has removeApp as className', () => {
    const deleteBtn = shallow(<AppRemove app="myapp"/>);
    expect(deleteBtn.find('.removeApp').length).toBe(1);
  });

  it('renders the confirmation on click', () => {
    const deleteBtn = shallow(<AppRemove app="myapp"/>);
    deleteBtn.find("a").simulate("click", fakeEvent);
    var confirmation = deleteBtn.find(AppRemoveConfirmation);
    expect(confirmation.length).toBe(1);
    expect(confirmation.props().app).toBe("myapp");
  });
});

describe('AppRemoveConfirmation', () => {
  beforeEach(() => {
    $.prototype.modal = jest.fn();
  });

  it('has modal as className', () => {
    const confirmation = mount(
      <AppRemoveConfirmation app="myapp" />
    );
    expect(confirmation.find(".modal").length).toBe(1);
  });

  it('is not confirmed when rendered', () => {
    const confirmation = mount(
      <AppRemoveConfirmation app="myapp" />
    );
    expect(confirmation.find(".btn-remove").props().disabled).toBe(true);
    expect(confirmation.state().isConfirmed).toBe(false);
  })

  it('is not confirmed if confirmation not fully typed', () => {
    const confirmation = mount(
      <AppRemoveConfirmation app="myapp" />
    );
    confirmation.find(".remove-confirmation").simulate("change", {
      target: {
        value: "mya"
      }
    });
    expect(confirmation.find(".btn-remove").props().disabled).toBe(true);
    expect(confirmation.state().isConfirmed).toBe(false);
  });

  it('is confirmed when confirmation is fully entered', () => {
    const confirmation = mount(
      <AppRemoveConfirmation app="myapp"/>
    );
    confirmation.find(".remove-confirmation").simulate("change", {
      target: {
        value: "myapp"
      }
    });
    expect(confirmation.find(".btn-remove").props().disabled).toBe(false);
    expect(confirmation.state().isConfirmed).toBe(true);
  });

  it('calls onClose when dialog is closed', () => {
    var onClose = jest.fn();
    const confirmation = mount(
      <AppRemoveConfirmation app="myapp" onClose={onClose}/>
    );
    confirmation.find(".close").simulate("click", { preventDefault() {}});
    confirmation.find(".cancel").simulate("click", { preventDefault() {}});
    expect(onClose.mock.calls.length).toBe(2);
  });

  it('call appRemove if is confirmed', () => {
    var appRemove = jest.fn();
    const confirmation = mount(
      <AppRemoveConfirmation app="myapp"/>
    );
    confirmation.find(".remove-confirmation").simulate("change", {
      target: {
        value: "myapp"
      }
    });
    confirmation.find(".btn-remove").simulate("click", appRemove);
    expect(appRemove.mock.calls.length).toBe(0);
  });
});

describe('AppUnlockConfirmation', () => {
  beforeEach(() => {
    $.prototype.modal = jest.fn();
  });

  it('is not confirmed when rendered', () => {
    const confirmation = mount(
      <AppUnlockConfirmation app="myapp"/>
    );
    expect(confirmation.find(".btn-unlock").props().disabled).toBe(true);
    expect(confirmation.state().isConfirmed).toBe(false);
  })

  it('is not confirmed if confirmation not fully typed', () => {
    const confirmation = mount(
      <AppUnlockConfirmation app="myapp"/>
    );
    confirmation.find(".unlock-confirmation").simulate("change", {
      target: {
        value: "mya"
      }
    });
    expect(confirmation.find(".btn-unlock").props().disabled).toBe(true);
    expect(confirmation.state().isConfirmed).toBe(false);
  });

  it('is confirmed when confirmation is fully entered', () => {
    const confirmation = mount(
      <AppUnlockConfirmation app="myapp"/>
    );
    confirmation.find(".unlock-confirmation").simulate("change", {
      target: {
        value: "myapp"
      }
    });
    expect(confirmation.find(".btn-unlock").props().disabled).toBe(false);
    expect(confirmation.state().isConfirmed).toBe(true);
  });

  it('calls onClose when dialog is closed', () => {
    var onClose = jest.fn();
    const confirmation = mount(
      <AppUnlockConfirmation app="myapp" onClose={onClose}/>
    );
    confirmation.find(".close").simulate("click", { preventDefault() {}});
    confirmation.find(".cancel").simulate("click", { preventDefault() {}});
    expect(onClose.mock.calls.length).toBe(2);
  });

  it('call appUnlock if is confirmed', () => {
    var appUnlock = jest.fn();
    const confirmation = mount(
      <AppUnlockConfirmation app="myapp"/>
    );
    confirmation.find(".unlock-confirmation").simulate("change", {
      target: {
        value: "myapp"
      }
    });
    confirmation.find(".btn-unlock").simulate("click", { preventDefault() {}});
    expect(appUnlock.mock.calls.length).toBe(0);
  });
});
