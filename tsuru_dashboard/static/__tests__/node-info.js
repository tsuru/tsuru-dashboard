import React from "react";
import { shallow, mount } from "enzyme";
import $ from "jquery";
import { Metrics } from "../jsx/components/metrics";
import { NodeInfo, Node, MetricsTab, ContainersTab, MetadataTab, DeleteNodeBtn , ContainerRow, DeleteNodeConfirmation } from "../jsx/components/node-info";
import { Tab, Tabs } from "../jsx/components/base";

describe('NodeInfo', () => {
  it('has node-container as className', () => {
    const nodeInfo = shallow(<NodeInfo url="url"/>);
    expect(nodeInfo.find(".node-container").length).toBe(1);
  });

  it('fetches the url from node data', () => {
    $.ajax = jest.genMockFunction();
    const nodeInfo = mount(<NodeInfo url="url"/>);
    expect($.ajax.mock.calls.length).toBe(1);
    expect($.ajax.mock.calls[0][0].url).toBe("url");
  });

  it('renders a Node with fetched data', () => {
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
    $.ajax = jest.genMockFunction().mockImplementation((p) => {
      p.success(data)
    });
    const nodeInfo = mount(<NodeInfo url="url"/>);
    var node = nodeInfo.find(Node);
    expect(node.length).toBe(1);
    expect(node.props().node).toEqual(data.node);
  });
});

describe('Node', () => {
  var nodeData = {
    info: {
      Status: "ready",
      Metadata: {
        pool: "pool"
      },
      Address: "http://127.0.0.1"
    },
    containers: [{
      Status: "started",
      LastStatusUpdate: "2016-05-11T21:40:52.615Z",
      BuildingImage: "",
      Version: "",
      Name: "tsuru-dashboard-67e5f5a8030600d33856",
      AppName: "tsuru-dashboard",
      IP: "172.17.0.3",
      Image: "127.0.0.1:5000/tsuru/app-tsuru-dashboard:v1",
      LastSuccessStatusUpdate: "2016-05-11T21:40:52.615Z",
      PrivateKey: "",
      Routable: false,
      ProcessName: "web",
      HostAddr: "127.0.0.1",
      LockedUntil: "0001-01-01T00:00:00Z",
      User: "",
      HostPort: "49153",
      MongoID: "56f921202b55bb887efd00db",
      Type: "python",
      ID: "b32c7754dd93e440d4fd36941677b11c865eeb12f3a43c7b1775fa31c642b85f"
    }]
  };

  it('has node as className', () => {
    const node = shallow(<Node node={nodeData}/>);
    expect(node.find(".node").length).toBe(1);
  });

  it('renders the tabs', () => {
    const node = shallow(<Node node={nodeData}/>);
    var tabs = node.find(Tabs);
    expect(tabs.props().tabs).toEqual(["Containers", "Metadata", "Metrics"]);
  });

  it('renders <ContainersTab/>', () => {
    const node = shallow(<Node node={nodeData}/>);
    var containers = node.find(ContainersTab);
    expect(containers.props().containers).toEqual(nodeData.containers);
  });

  it('renders <MetricsTab/>', () => {
    $.ajax = jest.genMockFunction();
    const node = mount(<Node node={nodeData}/>);
    node.find(Tab).at(2).find("a").simulate("click");
    expect(node.find(MetricsTab).length).toBe(1);
    expect(node.find(MetricsTab).props().addr).toBe("127.0.0.1");
  });

  it('renders <MetadataTab/>', () => {
    const node = mount(<Node node={nodeData}/>);
    node.find(Tab).at(1).find("a").simulate("click");
    expect(node.find(MetadataTab).length).toBe(1);
    expect(node.find(MetadataTab).props().metadata).toBe(nodeData.info.Metadata);
  });

  it('renders the h1 title', () => {
    const node = shallow(<Node node={nodeData}/>);
    expect(node.find("h1").text()).toBe("pool - http://127.0.0.1 - ready");
  });

  it('renders <DeleteNodeBtn/>', () => {
    const node = shallow(<Node node={nodeData}/>);
    expect(node.find(DeleteNodeBtn).length).toBe(1);
    expect(node.find(DeleteNodeBtn).props().addr).toBe("http://127.0.0.1");
  });
});

describe('ContainersTab', () => {
  var containersData = [{
      Status: "started",
      AppName: "tsuru-dashboard",
      DashboardURL: "/apps/tsuru-dashboard/",
      IP: "172.17.0.3",
      ProcessName: "web",
      HostPort: "49153",
      ID: "b32c7754dd93e440d4fd36941677b11c865eeb12f3a43c7b1775fa31c642b85f"
    },
    {
      Status: "started",
      AppName: "tsuru-dashboard2",
      DashboardURL: "/apps/tsuru-dashboard2/",
      IP: "172.17.0.2",
      ProcessName: "web",
      HostPort: "49152",
      ID: "40d4fd36941677b11c865eeb12f3a43c7b1775fa31c642b85fb32c7754dd93e4"
    }
  ];
  it('has containers as className', () => {
    const containers = shallow(<ContainersTab containers={containersData}/>);
    expect(containers.find(".containers").length).toBe(1);
  });

  it('renders one <ContainerRow/> for each container', () => {
    const containers = shallow(<ContainersTab containers={containersData}/>);
    var rows = containers.find(ContainerRow);
    expect(rows.length).toBe(2);
    expect(rows.first().props().container).toBe(containersData[0]);
    expect(rows.last().props().container).toBe(containersData[1]);
  });

  it('renders the app link', () => {
    const containers = mount(<ContainersTab containers={containersData}/>);
    expect(containers.find("a").first().props().href).toBe("/apps/tsuru-dashboard/");
  });

});

describe('MetadataTab', () => {
  it('renders a Tr for each metadata', () => {
    var data = {
      data1: "value1",
      data2: "value2",
      data3: "value3"
    };
    const metadata = shallow(<MetadataTab metadata={data}/>);
    expect(metadata.find("tr").length).toBe(3);
  });

});

describe('MetricsTab', () => {
  it('renders <Metrics/>', () => {
    const metricsTab = shallow(<MetricsTab addr="127.0.0.1"/>);
    var props = metricsTab.find(Metrics).props();
    expect(props.targetName).toBe("127.0.0.1");
    expect(props.targetType).toBe("node");
    expect(props.metrics).toEqual(["load", "cpu_max", "mem_max", "nettx", "netrx", "disk", "swap"]);
  });
});

describe('DeleteNodeBtn', () => {
  var fakeEvent = { preventDefault() {}, stopPropagation() {} };
  it('has deleteNode as className', () => {
    const deleteBtn = shallow(<DeleteNodeBtn addr="http://127.0.0.1"/>);
    expect(deleteBtn.find('.deleteNode').length).toBe(1);
  });

  it('renders the confirmation on click', () => {
    const deleteBtn = shallow(<DeleteNodeBtn addr="http://127.0.0.1" removeURL={"/remove"}/>);
    deleteBtn.find("a").simulate("click", fakeEvent);
    var confirmation = deleteBtn.find(DeleteNodeConfirmation);
    expect(confirmation.length).toBe(1);
    expect(confirmation.props().addr).toBe("http://127.0.0.1");
    expect(confirmation.props().removeAction).toBe("/remove");
  });
});

describe('DeleteNodeConfirmation', () => {

  it('has modal as className', () => {
    const confirmation = shallow(
      <DeleteNodeConfirmation addr="http://127.0.0.1"/>
    );
    expect(confirmation.find(".modal").length).toBe(1);
  });

  it('is not confirmed when rendered', () => {
    const confirmation = shallow(
      <DeleteNodeConfirmation addr="http://127.0.0.1"/>
    );
    expect(confirmation.find(".btn-remove").props().disabled).toBe(true);
    expect(confirmation.state().isConfirmed).toBe(false);
  })

  it('is not confirmed if confirmatio not fully typed', () => {
    const confirmation = shallow(
      <DeleteNodeConfirmation addr="http://127.0.0.1"/>
    );
    confirmation.find(".remove-confirmation").simulate("change", {
      target: {
        value: "http://127"
      }
    });
    expect(confirmation.find(".btn-remove").props().disabled).toBe(true);
    expect(confirmation.state().isConfirmed).toBe(false);
  });

  it('is confirmed when confirmation is fully entered', () => {
    const confirmation = shallow(
      <DeleteNodeConfirmation addr="http://127.0.0.1"/>
    );
    confirmation.find(".remove-confirmation").simulate("change", {
      target: {
        value: "http://127.0.0.1"
      }
    });
    expect(confirmation.find(".btn-remove").props().disabled).toBe(false);
    expect(confirmation.state().isConfirmed).toBe(true);
  });

  it('calls onClose when dialog is closed', () => {
    var onClose = jest.genMockFunction();
    const confirmation = shallow(
      <DeleteNodeConfirmation addr="http://127.0.0.1" onClose={onClose}/>
    );
    confirmation.find(".close").simulate("click", { preventDefault() {}});
    confirmation.find(".cancel").simulate("click", { preventDefault() {}});
    expect(onClose.mock.calls.length).toBe(2);
  });

  it('prevents form submition when not confirmed', () => {
    var mockEvent = {preventDefault: jest.genMockFunction()};
    const confirmation = shallow(
      <DeleteNodeConfirmation addr="http://127.0.0.1"/>
    );
    confirmation.find("form").simulate("submit", mockEvent);
    expect(mockEvent.preventDefault).toBeCalled();
  });

  it('submit form if is confirmed', () => {
    var mockEvent = {preventDefault: jest.genMockFunction()};
    const confirmation = shallow(
      <DeleteNodeConfirmation addr="http://127.0.0.1"/>
    );
    confirmation.find(".remove-confirmation").simulate("change", {
      target: {
        value: "http://127.0.0.1"
      }
    });
    confirmation.find("form").simulate("submit", mockEvent);
    expect(mockEvent.preventDefault.mock.calls.length).toBe(0);
  });

  it('handle changes on the checkboxes', () => {
    const confirmation = shallow(
      <DeleteNodeConfirmation addr="http://127.0.0.1"/>
    );
    expect(confirmation.state().rebalance).toBe(true);
    expect(confirmation.state().destroy).toBe(true);
    confirmation.find('input[name="rebalance"]').simulate("change", {
      target: {name: "rebalance"}
    });
    confirmation.find('input[name="destroy"]').simulate("change", {
      target: {name: "destroy"}
    });
    expect(confirmation.state().rebalance).toBe(false);
    expect(confirmation.state().destroy).toBe(false);
  });

  it('renders a form with correct action', () => {
    const confirmation = shallow(
      <DeleteNodeConfirmation addr="http://127.0.0.1" removeAction={"/remove"}/>
    );
    var form = confirmation.find("form");
    expect(form.length).toBe(1);
    expect(form.props().action).toBe("/remove");
  });
});
