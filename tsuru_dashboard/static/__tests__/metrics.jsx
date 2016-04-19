jest.dontMock('../jsx/components/metrics.jsx');


var React = require('react'),
    Enzyme = require('enzyme'),
    $ = require('jquery'),
    Module = require('../jsx/components/metrics.jsx'),
    Metrics = Module.Metrics,
    GraphContainer = Module.GraphContainer;

describe('Metrics', function() {
  it('has metrics as className', function() {
    const metrics = Enzyme.shallow(<Metrics />);

    expect(metrics.find(".metrics").length).toBe(1);
  });

  it('contains GraphContainers for all metrics', function() {
    const metrics = Enzyme.shallow(<Metrics />);
    var containers = metrics.find(GraphContainer);
    var kinds = containers.map(c => c.props().kind);
    var expectedKinds = [
      "cpu_max", "mem_max", "swap", "connections",
      "units", "requests_min", "response_time", "http_methods",
      "status_code", "nettx", "netrx"
    ];

    expect(containers.length).toBe(11);
    expect(kinds.sort()).toEqual(expectedKinds.sort());
  });
});

describe('GraphContainer', function() {
  it('has graph-container as className', function(){
    const graphContainer = Enzyme.shallow(<GraphContainer />);

    expect(graphContainer.find(".graph-container").length).toBe(1);
  });

  it('fetches application metrics', function() {
    $.getJSON.mockClear();
    const graphContainer = Enzyme.shallow(
      <GraphContainer kind="cpu_max" appName="myApp" processName="myProcess"/>
    );

    expect($.getJSON.mock.calls.length).toBe(1);
    expect($.getJSON.mock.calls[0][0]).toBe(
      "/metrics/app/myApp/?metric=cpu_max&interval=1m&date_range=1h&process_name=myProcess"
    );
  });

  it('renders the graph title', function() {
    const graphContainer = Enzyme.shallow(
      <GraphContainer title="This is a cool graph!"/>
    );

    expect(graphContainer.find("h2").text()).toBe("This is a cool graph!");
  });

  it('renders a link to the graph details', function() {
    const graphContainer = Enzyme.shallow(
      <GraphContainer kind="cpu_max" appName="myApp" processName="myProcess"/>
    );
    var aHref = graphContainer.find("a").first();

    expect(aHref.props().href).toBe("/apps/myApp/metrics/details/?kind=cpu_max&from=1h&serie=1m");
  });

  it('renders the graph div', function() {
    const graphContainer = Enzyme.shallow(<GraphContainer kind="cpu_max" />);
    var graph = graphContainer.find("div").last();

    expect(graph.props().id).toBe("cpu_max");
    expect(graph.props().className).toBe("graph");
  });
});
