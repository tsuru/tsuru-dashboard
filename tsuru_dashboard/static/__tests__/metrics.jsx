jest.dontMock('../jsx/components/metrics.jsx');


var React = require('react'),
    Enzyme = require('enzyme'),
    $ = require('jquery'),
    Module = require('../jsx/components/metrics.jsx'),
    Metrics = Module.Metrics,
    WebTransactionsMetrics = Module.WebTransactionsMetrics,
    GraphContainer = Module.GraphContainer,
    Graph = Module.Graph;

describe('Metrics', function() {

  beforeEach(() => {
    $.plot = jest.genMockFunction();
  });

  it('has metrics as className', function() {
    const metrics = Enzyme.shallow(<Metrics />);

    expect(metrics.find(".metrics").length).toBe(1);
  });

  it('contains GraphContainers for all metrics', function() {
    const metrics = Enzyme.shallow(<Metrics targetName="" />);
    var containers = metrics.find(GraphContainer);
    var ids = containers.map(c => c.props().id.substring(1));
    var expectedIds = ["cpu_max", "mem_max", "swap", "connections", "units"];

    expect(containers.length).toBe(5);
    expect(ids.sort()).toEqual(expectedIds.sort());
  });

  it('contains GraphContainer for a single metric', function() {
    const metrics = Enzyme.shallow(<Metrics targetName={"myApp"} metrics={["cpu_max"]} />);
    var containers = metrics.find(GraphContainer);

    expect(containers.length).toBe(1);
    expect(containers.props().id).toBe("myApp_cpu_max");
  });

  it('renders a GraphContainer with data url for app metrics', function() {
    const metrics = Enzyme.shallow(<Metrics targetName={"myApp"} processName={"myProcess"} metrics={["cpu_max"]} />);
    var container = metrics.find(GraphContainer);

    expect(container.props().data_url).toBe(
      "/metrics/app/myApp/?metric=cpu_max&interval=1m&date_range=1h&process_name=myProcess"
    );
  });

  it('renders a GraphContainer with data url for component metrics', function() {
    const metrics = Enzyme.shallow(<Metrics targetName={"myComp"} targetType={"component"} metrics={["cpu_max"]} />);
    var container = metrics.find(GraphContainer);

    expect(container.props().data_url).toBe(
      "/metrics/component/myComp/?metric=cpu_max&interval=1m&date_range=1h"
    );
  });

  it('sends new options to GraphContainer on change', function() {
    const metrics = Enzyme.mount(
      <Metrics targetName={"myApp"} targetType={"app"} metrics={["cpu_max"]} />
    );
    var container = metrics.find(GraphContainer);
    expect(container.props().data_url).toBe(
      "/metrics/app/myApp/?metric=cpu_max&interval=1m&date_range=1h"
    );
    metrics.find('select[name="from"]').simulate('change', {target: { value: "3h"}});
    expect(container.props().data_url).toBe(
      "/metrics/app/myApp/?metric=cpu_max&interval=1m&date_range=3h"
    );
    metrics.find('select[name="serie"]').simulate('change', {target: { value: "1d"}});
    expect(container.props().data_url).toBe(
      "/metrics/app/myApp/?metric=cpu_max&interval=1d&date_range=3h"
    );
    metrics.find('input[name="refresh"]').simulate('change', {target: { checked: true}});
    expect(container.props().refresh).toBe(true);
  });

  it('call onFromChange when from changes', function() {
    var onChange = jest.genMockFunction();
    const metrics = Enzyme.mount(
      <Metrics targetName={"myApp"} onFromChange={onChange} />
    );
    metrics.find('select[name="from"]').simulate('change', {target: { value: "3h"}});
    expect(onChange.mock.calls.length).toBe(1);
    expect(onChange.mock.calls[0][0]).toBe("3h");
  });

  it('renders a container div depending on the selected size', function() {
    const metrics = Enzyme.mount(<Metrics targetName={"myApp"} targetType={"app"} metrics={["cpu_max"]} />);
    var sizeSelector = metrics.find('select[name="size"]');
    expect(metrics.find('.graphs-small').length).toBe(1);
    sizeSelector.simulate('change', {target: { value: "medium"}});
    expect(metrics.find('.graphs-medium').length).toBe(1);
    sizeSelector.simulate('change', {target: { value: "large"}});
    expect(metrics.find('.graphs-large').length).toBe(1);
    sizeSelector.simulate('change', {target: { value: "small"}});
    expect(metrics.find('.graphs-small').length).toBe(1);
  });

  it('updates legend state depending on selected size', function() {
    const metrics = Enzyme.mount(<Metrics targetName={"myApp"} targetType={"app"} metrics={["cpu_max"]} />);
    var sizeSelector = metrics.find('select[name="size"]');
    expect(metrics.state().legend).toBe(false);
    sizeSelector.simulate('change', {target: { value: "large"}});
    expect(metrics.state().legend).toBe(true);
    sizeSelector.simulate('change', {target: { value: "medium"}});
    expect(metrics.state().legend).toBe(false);
  });

});

describe('WebTransactionsMetrics', function() {
  it('renders Metrics with correct props', function() {
    const webTransactions = Enzyme.shallow(<WebTransactionsMetrics appName={"myApp"}/>);
    var metrics = webTransactions.find(Metrics);
    expect(metrics.props().metrics).toEqual(
      ["requests_min", "response_time", "http_methods", "status_code", "nettx", "netrx"]
    );
    expect(metrics.props().targetName).toEqual("myApp");
    expect(metrics.props().targetType).toEqual("app");
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

  it('renders the Graph component', function() {
    const graphContainer = Enzyme.shallow(<GraphContainer id="cpu_max" />);
    var graph = graphContainer.find(Graph);

    expect(graph.props().id).toBe("cpu_max");
  });

  it('sends fetched data to child Graph', function() {
    var prev_get = $.getJSON;
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
    $.getJSON = prev_get;
  });

  it('re-fetches data when props change', function() {
    const graphContainer = Enzyme.mount(
      <GraphContainer data_url={"/metrics?call=1"}/>
    );
    graphContainer.setProps({ data_url: "/metrics?call=2"});

    expect($.getJSON.mock.calls.length).toBe(2);
    expect($.getJSON.mock.calls[0][0]).toBe("/metrics?call=1");
    expect($.getJSON.mock.calls[1][0]).toBe("/metrics?call=2");
  });

  it('manages interval according to refresh prop', function() {
    const graphContainer = Enzyme.mount(
      <GraphContainer data_url={"/metrics?call=1"} refresh={true}/>
    );

    expect(setInterval.mock.calls.length).toBe(1);
    expect(setInterval.mock.calls[0][1]).toBe(60000);
    expect(clearInterval.mock.calls.length).toBe(0);

    graphContainer.setProps({ data_url: "/metrics?call=1", refresh: false});
    expect(clearInterval.mock.calls.length).toBe(1);
  })

  it('re-fetches data when refresh is on', function() {
    const graphContainer = Enzyme.mount(
      <GraphContainer data_url={"/metrics?call=1"} refresh={true}/>
    );
    expect($.getJSON.mock.calls.length).toBe(1);
    jest.runOnlyPendingTimers();
    expect($.getJSON.mock.calls.length).toBe(2);
    jest.runOnlyPendingTimers();
    expect($.getJSON.mock.calls.length).toBe(3);
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
