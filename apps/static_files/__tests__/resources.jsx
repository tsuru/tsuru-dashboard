jest.dontMock('../jsx/components/resources.jsx');

var React = require('react/addons'),
    Resources = require('../jsx/components/resources.jsx'),
    TestUtils = React.addons.TestUtils;

describe('Resources', function() {
  it('should has resources as className', function() {
    var list = TestUtils.renderIntoDocument(
      <Resources />
    );
    
    expect(list.getDOMNode("div").className).toEqual("resources");
  });
});
