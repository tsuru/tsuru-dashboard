jest.dontMock('../jsx/components/loading.jsx');

describe('Loading', function() {
  it('changes the text after click', function() {
    var React = require('react');
    var ReactDOM = require('react-dom');
    var Loading = require('../jsx/components/loading.jsx');
    var TestUtils = require('react-addons-test-utils');

    var loading = TestUtils.renderIntoDocument(
      <Loading />
    );
    
    expect(ReactDOM.findDOMNode(loading).className).toEqual("loader");
  });
});
