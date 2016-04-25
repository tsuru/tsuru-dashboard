jest.dontMock("../jsx/components/component-list.jsx");

var React = require('react'),
    Enzyme = require('enzyme'),
    $ = require('jquery'),
    Module = require("../jsx/components/component-list.jsx"),
    ComponentList = Module.ComponentList,
    Component = Module.Component,
    Metrics = require("../jsx/components/metrics.jsx").Metrics;

describe('ComponentList', function() {
    it('fetches the components url', function() {
        const componentList = Enzyme.mount(
            <ComponentList url={"components.json"}/>
        );

        expect($.ajax.mock.calls.length).toBe(1);
        expect($.ajax.mock.calls[0][0].url).toBe("components.json");
    });

    it('has component-list as classname', function() {
        const componentList = Enzyme.shallow(<ComponentList />);

        expect(componentList.find(".component-list").length).toBe(1);
    });

    it('renders a component for each one that was fetched', function() {
        $.ajax = function(obj) {
            obj.success({components: ["registry", "big-sibling"]});
        };
        const componentList = Enzyme.mount(<ComponentList />);
        var components = componentList.find(Component);

        expect(components.length).toBe(2);
        expect(components.first().props().name).toBe("registry");
        expect(components.last().props().name).toBe("big-sibling");
    });
});

describe('Component', function() {
    it('renders Metrics for the component', function() {
        const component = Enzyme.mount(
            <Component name={"big-sibling"}/>
        );
        var metrics = component.find(Metrics);

        expect(metrics.length).toBe(1);
        expect(metrics.props().targetName).toBe("big-sibling");
        expect(metrics.props().targetType).toBe("component");
    });

    it('has component as classname', function() {
        const component = Enzyme.shallow(<Component />);

        expect(component.find(".component").length).toBe(1);
    });
});
