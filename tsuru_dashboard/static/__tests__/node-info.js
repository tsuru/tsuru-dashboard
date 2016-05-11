jest.dontMock('../jsx/components/node-info.jsx');


var React = require('react'),
    Enzyme = require('enzyme'),
    $ = require('jquery'),
    Module = require('../jsx/components/node-info.jsx'),
    NodeInfo = Module.NodeInfo,
    Node = Module.Node;

describe('NodeInfo', function() {
    it('has node-container as className', function() {
        const nodeInfo = Enzyme.shallow(<NodeInfo url="url"/>);
        expect(nodeInfo.find(".node-container").length).toBe(1);
    });

    it('fetches the url from node data', function() {
        const nodeInfo = Enzyme.mount(<NodeInfo url="url"/>);
        expect($.ajax.mock.calls.length).toBe(1);
        expect($.ajax.mock.calls[0][0].url).toBe("url");
    });

    it('renders a Node with fetched data', function() {
        var data = {
            node: {
                info: {
                    Status: "ready",
                    Metadata: {
                        pool: "pool"
                    },
                    Address: "http://127.0.0.1"
                },
                containers: []
            }
        };
        $.ajax = jest.genMockFunction().mockImplementation(function(p) {
            p.success(data)
        });
        const nodeInfo = Enzyme.mount(<NodeInfo url="url"/>);
        var node = nodeInfo.find(Node);
        expect(node.length).toBe(1);
        expect(node.props().node).toEqual(data.node);
    });

});
