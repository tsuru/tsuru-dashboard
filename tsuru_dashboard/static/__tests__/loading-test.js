jest.dontMock('../jsx/components/loading.jsx');

var React = require('react'),
    Enzyme = require('enzyme'),
    Loading = require('../jsx/components/loading.jsx');

describe('Loading', function() {
  it('renders an element with "loader" class', function() {
    var wrapper = Enzyme.shallow(<Loading />)
    expect(wrapper.find(".loader").length).toBe(1);
  });
});
