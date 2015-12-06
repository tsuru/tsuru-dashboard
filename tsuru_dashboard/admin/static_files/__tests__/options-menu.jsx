jest.dontMock('../jsx/components/options-menu.jsx');

var React = require('react'),
    ReactDOM = require('react-dom'),
    OptionsMenu = require('../jsx/components/options-menu.jsx'),
    TestUtils = require('react-addons-test-utils');

describe('OptionMenu', function() {
  it('should has options-menu as className', function() {
    var optionsMenu = TestUtils.renderIntoDocument(
      <OptionsMenu />
    );

    expect(ReactDOM.findDOMNode(optionsMenu).className).toEqual("options-menu");
  });

  it('options items', function() {
    var optionsMenu = TestUtils.renderIntoDocument(
      <OptionsMenu items={["about", "docs"]} />
    );

    var items = TestUtils.scryRenderedDOMComponentsWithClass(optionsMenu, 'options-item');
    expect(items.length).toBe(2);
  });
});
