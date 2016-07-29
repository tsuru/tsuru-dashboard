// jest.dontMock('../jsx/components/node-create.jsx');
//
// var React = require('react'),
//     Enzyme = require('enzyme'),
//     NodeCreate = require('../jsx/components/node-create.jsx');
//
// describe('NodeCreate', function() {
//   it('should has node-create as className', function() {
//     const nodeCreate = Enzyme.shallow(<NodeCreate />);
//     expect(nodeCreate.find(".node-create").length).toBe(1);
//   });
//
//   it('should initial state', function() {
//     const nodeCreate = Enzyme.shallow(<NodeCreate />);
//     var state = nodeCreate.state();
//     expect(state.templates.length).toBe(0);
//     expect(state.metadata.length).toBe(0);
//     expect(state.register).toBeFalsy();
//   });
//
//   it('change register state on click', function() {
//     const nodeCreate = Enzyme.mount(<NodeCreate />);
//     var register = nodeCreate.find(".register");
//
//     expect(nodeCreate.state().register).toBeFalsy();
//     expect(nodeCreate.state().metadata.length).toEqual(0);
//
//     register.simulate('click');
//     expect(nodeCreate.state().register).toBeTruthy();
//     expect(nodeCreate.state().metadata).toEqual([{id: 1, key: "address", value: ""}]);
//
//     register.simulate('click');
//     expect(nodeCreate.state().register).toBeFalsy();
//     expect(nodeCreate.state().metadata).toEqual([]);
//   });
//
//   it('don"t show template select on empty templates', function() {
//     const nodeCreate = Enzyme.shallow(<NodeCreate />);
//     var templates = nodeCreate.find(".template");
//     expect(templates.length).toBe(0);
//   });
//
//   it('metadata items', function() {
//     const nodeCreate = Enzyme.mount(<NodeCreate />);
//
//     nodeCreate.get(0).addMetadata("key", "value");
//     nodeCreate.get(0).addMetadata("anotherkey", "v");
//
//     var items = nodeCreate.find(".meta-item");
//     expect(items.length).toEqual(2);
//
//     var inputs = items.children().find("input");
//     expect(inputs.at(0).props().value).toBe("key");
//     expect(inputs.at(1).props().value).toBe("value");
//
//     expect(inputs.at(2).props().value).toBe("anotherkey");
//     expect(inputs.at(3).props().value).toBe("v");
//   });
//
// });
