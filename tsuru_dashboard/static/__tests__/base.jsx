// jest.dontMock('../jsx/components/base.jsx');
//
// var React = require('react'),
//     Enzyme = require('enzyme'),
//     Tab = require('../jsx/components/base.jsx').Tab,
//     Tabs = require('../jsx/components/base.jsx').Tabs;
//
// describe('Tabs', function() {
//   it('should render a tab with correct name', function() {
//     const tabs = Enzyme.shallow(<Tabs tabs={["tab1"]}/>);
//     var tab = tabs.find(Tab);
//     expect(tab.props().name).toBe("tab1");
//   });
//
//   it('should render a Tab for each element', function() {
//     const tabs = Enzyme.shallow(<Tabs tabs={["tab1", "tab2"]}/>);
//     expect(tabs.find(Tab).length).toBe(2);
//   });
// });
//
// describe('Tab', function() {
//   it('has no className if its not active', function() {
//     const tab = Enzyme.shallow(<Tab name={"tab"} active={false} />);
//     expect(tab.find(".active").length).toBe(0);
//   });
//
//   it('has className active if its active', function() {
//     const tab = Enzyme.shallow(<Tab name={"tab"} active={true} />);
//     expect(tab.find(".active").length).toBe(1);
//   });
//
//   it('triggers setActive on click', function() {
//     var setActive = jest.genMockFunction();
//     const tab = Enzyme.mount(<Tab name={"tab"} active={false} setActive={setActive}/>);
//     expect(setActive.mock.calls.length).toBe(0);
//     tab.find("a").simulate("click");
//     expect(setActive.mock.calls.length).toBe(1);
//   });
// });
