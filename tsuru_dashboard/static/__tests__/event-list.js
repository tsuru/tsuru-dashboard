import React from "react";
import { shallow } from "enzyme";
import { EventFilters } from "../js/src/components/event-list";

describe('<EventFilters />', () => {
  it('initial state', () => {
    const filters = shallow(<EventFilters />);
    expect(filters.prop('id')).toBe("filter");
  });
});
