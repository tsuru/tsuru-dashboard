import React from "react";
import { shallow, mount } from "enzyme";
import { PoolRebalance } from "../js/src/components/pool-rebalance";
import sinon from "sinon";
import Cookies from 'js-cookie';

Cookies.get = jest.fn()
        .mockImplementation(() => 'csrftokentest');

describe("PoolRebalance", () => {
  describe("initial state", () => {
    it("displays a PoolRebalanceConfirmation", () => {
      const poolRebalance = shallow(<PoolRebalance />);
      expect(poolRebalance.find("PoolRebalanceConfirmation").length).toEqual(1);
    });
  });

  describe("confirmation", () => {
    it("displays a disabled confirmation button", () => {
      const poolRebalance = mount(<PoolRebalance />);
      const button = poolRebalance.find(".btn-rebalance");
      expect(button.length).toEqual(1);
      expect(button.props().disabled).toEqual("disabled");
    });

    it("enables the confirmation button when the correct pool name is set", () => {
      const poolRebalance = mount(<PoolRebalance poolName="mypool" />);
      const input = poolRebalance.find("input").at(0);

      input.instance().value = "wrong pool name";
      input.simulate("change", input);
      expect(poolRebalance.find(".btn-rebalance").at(0).props().disabled).toEqual("disabled");

      input.instance().value = "mypool";
      input.simulate("change", input);
      expect(poolRebalance.find(".btn-rebalance").at(0).props().disabled).toEqual("");
    });

    it("hides after clicking the cancel button", () => {
      const hideFunc = spyOn(PoolRebalance.prototype, "hide");
      const poolRebalance = mount(<PoolRebalance />);
      const cancelButton = poolRebalance.find(".btn").filterWhere(n => n.text() === "Cancel");
      expect(cancelButton.length).toEqual(1);

      cancelButton.simulate("click");
      expect(hideFunc).toHaveBeenCalled();
    });

    it("starts rebalance after confirmation", () => {
      const rebalanceFunc = spyOn(PoolRebalance.prototype, "rebalance");
      const poolRebalance = mount(<PoolRebalance poolName="mypool" />);
      const input = poolRebalance.find("input");
      expect(input.length).toEqual(1);
      const button = poolRebalance.find(".btn-rebalance");
      expect(button.length).toEqual(1);
      input.at(0).instance().value = "mypool";
      input.simulate("change", input);

      button.simulate("click");
      expect(rebalanceFunc).toHaveBeenCalled();
    });
  });

  describe("rebalance", () => {
    var xhr, requests;

    beforeEach(() => {
      xhr =  sinon.useFakeXMLHttpRequest();
      requests = [];
      xhr.onCreate = (req) => { requests.push(req) };
    });

    afterEach(() => {
      xhr.restore();
    });

    it("makes a request to rebalance route", () => {
      const poolRebalance = mount(<PoolRebalance url="/rebalance" />);

      poolRebalance.instance().startRebalance();
      expect(requests.length).toEqual(1);
      expect(requests[0].method).toEqual("POST");
      expect(requests[0].url).toEqual("/rebalance");
    });

    it("outputs the API response stream", () => {
      const poolRebalance = mount(<PoolRebalance url="/rebalance" />);
      poolRebalance.instance().startRebalance();
      poolRebalance.update();
      const output = poolRebalance.find("Output");
      expect(output.length).toEqual(1);
      expect(output.at(0).text()).toEqual("Wait until rebalance is started.");

      requests[0].respond(200, {"Content-Type": "application/x-json-stream"}, "starting rebalance");
      expect(output.text()).toEqual("starting rebalance");
    });
  });
});
