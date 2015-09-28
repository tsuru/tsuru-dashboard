jest.dontMock('../jsx/components/loading.jsx');
describe('Loading', function() {
  it('changes the text after click', function() {
    var React = require('react/addons');
    var Loading = require('../jsx/components/loading.jsx');
    var TestUtils = React.addons.TestUtils;

    var loading = TestUtils.renderIntoDocument(
      <Loading />
    );
    
    expect(loading.getDOMNode("div").className).toEqual("loader");
  });
});
