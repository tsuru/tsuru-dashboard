jest.dontMock('../jsx/components/metrics.jsx');


var React = require('react'),
    Enzyme = require('enzyme'),
    $ = require('jquery'),
    Module = require('../jsx/components/metrics.jsx'),
    Metrics = Module.Metrics,
    GraphContainer = Module.GraphContainer,
    Graph = Module.Graph;

describe('Metrics', function() {
  it('has metrics as className', function() {
    const metrics = Enzyme.shallow(<Metrics />);

    expect(metrics.find(".metrics").length).toBe(1);
  });

  it('contains GraphContainers for all metrics', function() {
    const metrics = Enzyme.shallow(<Metrics targetName="" />);
    var containers = metrics.find(GraphContainer);
    var ids = containers.map(c => c.props().id.substring(1));
    var expectedIds = [
      "cpu_max", "mem_max", "swap", "connections",
      "units", "requests_min", "response_time", "http_methods",
      "status_code", "nettx", "netrx"
    ];

    expect(containers.length).toBe(11);
    expect(ids.sort()).toEqual(expectedIds.sort());
  });

  it('contains GraphContainer for a single metric', function() {
    const metrics = Enzyme.shallow(<Metrics targetName={"myApp"} metrics={["cpu_max"]} />);
    var containers = metrics.find(GraphContainer);

    expect(containers.length).toBe(1);
    expect(containers.props().id).toBe("myApp_cpu_max");
  });

  it('renders a GraphContainer with urls for application metrics', function() {
    $.inArray.mockReturnValueOnce(-1);
    const metrics = Enzyme.shallow(<Metrics targetName={"myApp"} processName={"myProcess"} metrics={["cpu_max"]} />);
    var container = metrics.find(GraphContainer);

    expect(container.props().data_url).toBe(
      "/metrics/app/myApp/?metric=cpu_max&interval=1m&date_range=1h&process_name=myProcess"
    );
    expect(container.props().detail_url).toBe(
      "/apps/myApp/metrics/details/?kind=cpu_max&from=1h&serie=1m"
    );
  });

  it('ignores processName when inArray returns 1', function(){
    $.inArray.mockReturnValueOnce(1);
    const metrics = Enzyme.shallow(<Metrics targetName={"myApp"} processName={"myProcess"} metrics={["requests_min"]} />);
    var container = metrics.find(GraphContainer);

    expect(container.props().data_url).toBe(
      "/metrics/app/myApp/?metric=requests_min&interval=1m&date_range=1h"
    );
  });

  it('renders a GraphContainer with url for component metrics', function() {
    const metrics = Enzyme.shallow(<Metrics targetName={"myComp"} targetType={"component"} metrics={["cpu_max"]} />);
    var container = metrics.find(GraphContainer);

    expect(container.props().data_url).toBe(
      "/metrics/component/myComp/?metric=cpu_max&interval=1m&date_range=1h"
    );
    expect(container.props().detail_url).toBe(
      "/components/myComp/metrics/details/?kind=cpu_max&from=1h&serie=1m"
    );
  });

});

describe('GraphContainer', function() {

  beforeEach(() => {
    $.plot = jest.genMockFunction();
    $.getJSON.mockClear();
  });

  it('has graph-container as className', function(){
    const graphContainer = Enzyme.shallow(<GraphContainer />);

    expect(graphContainer.find(".graph-container").length).toBe(1);
  });

  it('fetches the data url', function() {
    const graphContainer = Enzyme.mount(
      <GraphContainer data_url={"/metrics/app/myApp/?metric=cpu_max&interval=1m&date_range=1h&process_name=myProcess"}/>
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
      <GraphContainer detail_url={"/apps/myApp/metrics/details/?kind=cpu_max&from=1h&serie=1m"}/>
    );
    var aHref = graphContainer.find("a").first();

    expect(aHref.props().href).toBe("/apps/myApp/metrics/details/?kind=cpu_max&from=1h&serie=1m");
  });

  it('renders the Graph component', function() {
    const graphContainer = Enzyme.shallow(<GraphContainer id="cpu_max" />);
    var graph = graphContainer.find(Graph);

    expect(graph.props().id).toBe("cpu_max");
  });

  it('sends fetched data to child Graph', function() {
    var data = {
      max: 1.5,
      data: {
        max: [[0,1], [1,1.5]],
        min: [[0,0.5], [1,1]]
      },
      min: 0
    };
    $.getJSON = function(url, callback) {
      callback(data);
    };

    const graphContainer = Enzyme.mount(<GraphContainer kind="cpu_max" />);
    var graph = graphContainer.find(Graph);

    expect(graph.props().model).toBe(data.data);
  });

});

describe('Graph', function() {

  beforeEach(() => {
    $.plot = jest.genMockFunction();
  });

  it('has graph as className', function() {
    const graph = Enzyme.shallow(<Graph />);

    expect(graph.find(".graph").length).toBe(1);
  });

  it('renders a div with the specified id', function() {
    const graph = Enzyme.shallow(<Graph id="123"/>);

    expect(graph.find("div").props().id).toBe("123");
  });

  it('uses flot on the rendered div', function() {
    var data = {
      max: [[0,1], [1,1.5]],
      min: [[0,0.5], [1,1]]
    }
    const graph = Enzyme.mount(<Graph id="123" model={data}/>);
    var call = $.plot.mock.calls[0];

    expect($.plot.mock.calls.length).toBe(1);
    expect(call[1].length).toBe(2);
    expect(call[1][0].data).toBe(data.max);
    expect(call[1][1].data).toBe(data.min);
    expect(call[2].legend.show).toBe(graph.props().legend);
  });

});
