jest.dontMock('../jsx/components/options-menu.jsx');

var React = require('react'),
    Enzyme = require('enzyme'),
    OptionsMenu = require('../jsx/components/options-menu.jsx');

describe('OptionMenu', function() {
  it('has options-menu as className', function() {
    const optionsMenu = Enzyme.shallow(<OptionsMenu />);
    expect(optionsMenu.find(".options-menu").length).toBe(1);
  });

  it('contains options items', function() {
    const optionsMenu = Enzyme.mount(
      <OptionsMenu items={["about", "docs"]} />
    );
    expect(optionsMenu.find('.options-item').length).toBe(2);
  });
});
