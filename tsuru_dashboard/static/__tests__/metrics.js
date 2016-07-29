import React from "react";
import { shallow, mount } from "enzyme";
import $ from "jquery";
import { Metrics, WebTransactionsMetrics, GraphContainer, Graph } from "../jsx/components/metrics";
import { Loading } from "../jsx/components/loading";

describe('Metrics', () => {
  beforeEach(() => {
    $.plot = jest.genMockFunction();
  });

  it('has metrics as className', () => {
    const metrics = shallow(<Metrics targetName=""/>);

    expect(metrics.find(".metrics").length).toBe(1);
  });

  it('contains GraphContainers for all metrics', () => {
    const metrics = shallow(<Metrics targetName="" />);
    var containers = metrics.find(GraphContainer);
    var ids = containers.map(c => c.props().id.substring(1));
    var expectedIds = ["cpu_max", "mem_max", "swap", "connections", "units"];

    expect(containers.length).toBe(5);
    expect(ids.sort()).toEqual(expectedIds.sort());
  });

  it('contains GraphContainer for a single metric', () => {
    const metrics = shallow(<Metrics targetName={"myApp"} metrics={["cpu_max"]} />);
    var containers = metrics.find(GraphContainer);

    expect(containers.length).toBe(1);
    expect(containers.props().id).toBe("myApp_cpu_max");
  });

  it('renders a GraphContainer with data url for app metrics', () => {
    const metrics = shallow(<Metrics targetName={"myApp"} processName={"myProcess"} metrics={["cpu_max"]} />);
    var container = metrics.find(GraphContainer);

    expect(container.props().data_url).toBe(
      "/metrics/app/myApp/?metric=cpu_max&interval=1m&date_range=1h&process_name=myProcess"
    );
  });

  it('renders a GraphContainer with data url for component metrics', () => {
    const metrics = shallow(<Metrics targetName={"myComp"} targetType={"component"} metrics={["cpu_max"]} />);
    var container = metrics.find(GraphContainer);

    expect(container.props().data_url).toBe(
      "/metrics/component/myComp/?metric=cpu_max&interval=1m&date_range=1h"
    );
  });

  it('sends new options to GraphContainer on change', () => {
    const metrics = mount(
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

  it('call onFromChange when from changes', () => {
    var onChange = jest.genMockFunction();
    const metrics = mount(
      <Metrics targetName={"myApp"} onFromChange={onChange} />
    );
    metrics.find('select[name="from"]').simulate('change', {target: { value: "3h"}});
    expect(onChange.mock.calls.length).toBe(1);
    expect(onChange.mock.calls[0][0]).toBe("3h");
  });

  it('renders a container div depending on the selected size', () => {
    const metrics = mount(<Metrics targetName={"myApp"} targetType={"app"} metrics={["cpu_max"]} />);
    var sizeSelector = metrics.find('select[name="size"]');

    expect(metrics.find('.graphs-small').length).toBe(1);
    sizeSelector.simulate('change', {target: { value: "medium"}});
    expect(metrics.find('.graphs-medium').length).toBe(1);
    sizeSelector.simulate('change', {target: { value: "large"}});
    expect(metrics.find('.graphs-large').length).toBe(1);
    sizeSelector.simulate('change', {target: { value: "small"}});
    expect(metrics.find('.graphs-small').length).toBe(1);
  });

  it('updates legend state depending on selected size', () => {
    const metrics = mount(<Metrics targetName={"myApp"} targetType={"app"} metrics={["cpu_max"]} />);
    var sizeSelector = metrics.find('select[name="size"]');

    expect(metrics.state().legend).toBe(false);
    sizeSelector.simulate('change', {target: { value: "large"}});
    expect(metrics.state().legend).toBe(true);
    sizeSelector.simulate('change', {target: { value: "medium"}});
    expect(metrics.state().legend).toBe(false);
  });

  it('renders <Loading/> when graphs are loading', () => {
    var getJSON = $.getJSON;
    $.getJSON = jest.fn((url, callback) => {});

    const metrics = mount(<Metrics targetName={"myApp"} targetType={"app"} metrics={["cpu_max"]} />);

    expect(metrics.find(Loading).length).toBe(1);
    $.getJSON = getJSON;
  });

  it('doesnt renders <Loading/> when graphs finish loading', () => {
    var getJSON = $.getJSON;
    $.getJSON = jest.fn((url, callback) => {callback({data: {}})});

    const metrics = mount(<Metrics targetName={"myApp"} targetType={"app"} metrics={["cpu_max"]} />);

    expect(metrics.find(Loading).length).toBe(0);
    $.getJSON = getJSON;
  });

});

describe('WebTransactionsMetrics', () => {
  it('renders Metrics with correct props', () => {
    const webTransactions = shallow(<WebTransactionsMetrics appName={"myApp"}/>);
    var metrics = webTransactions.find(Metrics);

    expect(metrics.props().metrics).toEqual(
      ["requests_min", "response_time", "http_methods", "status_code", "nettx", "netrx"]
    );
    expect(metrics.props().targetName).toEqual("myApp");
    expect(metrics.props().targetType).toEqual("app");
  });
});

describe('GraphContainer', () => {
  var data = {
    max: 1.5,
    data: {
      max: [[0,1], [1,1.5]],
      min: [[0,0.5], [1,1]]
    },
    min: 0
  };
  beforeEach(() => {
    $.plot = jest.genMockFunction();
    $.getJSON = jest.fn((url, callback) => {
      callback(data);
    });
  });

  it('has graph-container as className', () => {
    const graphContainer = mount(<GraphContainer data_url={"/"}/>);

    expect(graphContainer.find(".graph-container").length).toBe(1);
  });

  it('fetches the data url', () => {
    var loadMock = jest.genMockFunction();
    const graphContainer = mount(
      <GraphContainer data_url={"/metrics/app/myApp/?metric=cpu_max&interval=1m&date_range=1h&process_name=myProcess"}
        onLoad={loadMock}
      />
    );

    expect($.getJSON.mock.calls.length).toBe(1);
    expect($.getJSON.mock.calls[0][0]).toBe(
      "/metrics/app/myApp/?metric=cpu_max&interval=1m&date_range=1h&process_name=myProcess"
    );
    expect(loadMock.mock.calls.length).toBe(2);
    expect(loadMock.mock.calls[0][0]).toBe(true);
    expect(loadMock.mock.calls[1][0]).toBe(false);
  });

  it('renders the graph title', () => {
    const graphContainer = mount(
      <GraphContainer title="This is a cool graph!" data_url={"url"}/>
    );

    expect(graphContainer.find("h2").text()).toBe("This is a cool graph!");
  });

  it('renders the Graph component', () => {
    const graphContainer = mount(<GraphContainer id="cpu_max" data_url={"url"}/>);
    var graph = graphContainer.find(Graph);

    expect(graph.props().id).toBe("cpu_max");
  });

  it('sends fetched data to child Graph', () => {
    const graphContainer = mount(<GraphContainer kind="cpu_max" data_url={"url"}/>);
    var graph = graphContainer.find(Graph);

    expect(graph.props().model).toBe(data.data);
  });

  it('re-fetches data when props change', () => {
    const graphContainer = mount(
      <GraphContainer data_url={"/metrics?call=1"}/>
    );
    graphContainer.setProps({ data_url: "/metrics?call=2"});

    expect($.getJSON.mock.calls.length).toBe(2);
    expect($.getJSON.mock.calls[0][0]).toBe("/metrics?call=1");
    expect($.getJSON.mock.calls[1][0]).toBe("/metrics?call=2");
  });

  it('manages interval according to refresh prop', () => {
    const graphContainer = mount(
      <GraphContainer data_url={"/metrics?call=1"} refresh={true}/>
    );

    expect(setInterval.mock.calls.length).toBe(1);
    expect(setInterval.mock.calls[0][1]).toBe(60000);
    expect(clearInterval.mock.calls.length).toBe(0);

    graphContainer.setProps({ data_url: "/metrics?call=1", refresh: false});
    expect(clearInterval.mock.calls.length).toBe(1);
  })

  it('re-fetches data when refresh is on', () => {
    const graphContainer = mount(
      <GraphContainer data_url={"/metrics?call=1"} refresh={true}/>
    );

    expect($.getJSON.mock.calls.length).toBe(1);
    jest.runOnlyPendingTimers();
    expect($.getJSON.mock.calls.length).toBe(2);
    jest.runOnlyPendingTimers();
    expect($.getJSON.mock.calls.length).toBe(3);
  });

  it('doesnt renders when no data is fetched', () => {
    $.getJSON = jest.fn((url, callback) => {
      callback({data: {}});
    });
    const graphContainer = mount(<GraphContainer data_url={"/"}/>);
    expect(graphContainer.find(".graph-container").length).toBe(0);
  });

  it('clears the timer when unmounting', () => {
    const graphContainer = mount(
      <GraphContainer data_url={"/"} refresh={true}/>
    );
    expect(clearInterval.mock.calls.length).toBe(0);
    graphContainer.unmount();
    expect(clearInterval.mock.calls.length).toBe(1);
  });

});

describe('Graph', () => {

  beforeEach(() => {
    $.plot = jest.genMockFunction();
  });

  it('has graph as className', () => {
    const graph = shallow(<Graph />);

    expect(graph.find(".graph").length).toBe(1);
  });

  it('renders a div with the specified id', () => {
    const graph = shallow(<Graph id="123"/>);

    expect(graph.find("div").props().id).toBe("123");
  });

  it('uses flot on the rendered div', () => {
    var data = {
      max: [[0,1], [1,1.5]],
      min: [[0,0.5], [1,1]]
    }
    const graph = mount(<Graph id="123" model={data}/>);
    var call = $.plot.mock.calls[0];

    expect($.plot.mock.calls.length).toBe(1);
    expect(call[1].length).toBe(2);
    expect(call[1][0].data).toBe(data.max);
    expect(call[1][1].data).toBe(data.min);
    expect(call[2].legend.show).toBe(graph.props().legend);
  });

});
