jest.dontMock('../jsx/components/log.jsx');
jest.dontMock('oboe');

var React = require('react'),
    Enzyme = require('enzyme'),
    Log = require('../jsx/components/log.jsx');

describe('Log', function() {
  it('should has log as classname', function() {
    var wrapper = Enzyme.mount(<Log />);
    wrapper.setState({logging: true});
    expect(wrapper.children().find(".log").length).toBe(1);
  });
});
