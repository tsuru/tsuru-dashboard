import React, { Component } from "react";

class SelectTopInterval extends Component {
  constructor(props) {
    super(props);

    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(e) {
    e.preventDefault();
    var topSize = e.target.value.trim();
    this.props.selectTopRequests(this.props.requests, topSize);
  }

  render() {
    return (
      <select onChange={this.handleChange}>
      <option value="10">10</option>
      <option value="20">20</option>
      <option value="30">30</option>
      <option value="40">40</option>
      <option value="50">50</option>
      </select>
    );
  }
}

class RequestRow extends Component {
  render() {
    return (
      <tr>
      <td>{this.props.request.method}</td>
      <td>{this.props.request.path}</td>
      <td>{this.props.request.status_code}</td>
      <td>{this.props.request.response}</td>
      <td>{this.props.request.time}</td>
      </tr>
    )
  }
}

class TopTable extends Component {
  render() {
    var topRequests = this.props.top.map((result) => {
      return (
        <RequestRow key={result.method + result.path + result.status_code + result.time} request={result} />
      );
    });
    return (
      <table className="table">
      <thead>
      <tr>
      <th>Method</th>
      <th>Path</th>
      <th>Status Code</th>
      <th>Response time</th>
      <th>Time</th>
      </tr>
      </thead>
      <tbody>
      {topRequests.length > 0 ? topRequests : <tr><td colSpan="5">No requests found.</td></tr>}
      </tbody>
      </table>
    )
  }
}

export class TopSlow extends Component {
  constructor(props) {
    super(props);

    this.state = {top: [], requests: []};
  }

  componentDidMount() {
    this.loadData(this.props.from);
  }

  componentWillReceiveProps(nextProps) {
    if(this.props.from !== nextProps.from){
      this.loadData(nextProps.from);
    }
  }

  loadData(from) {
    var appName = this.props.appName;
    var kind = this.props.kind;
    var url = "/metrics/app/" + appName + "/?metric=" + kind + "&date_range=" + from;
    $.getJSON(url, (data) => {
      this.sortData(data);
    });
  }

  sortData(result) {
    var requests = [];
    for(let key in result.data) {
      for(let i in result.data[key]){
        var dt = new Date(result.data[key][i][0]);
        var date = dt.toString().split(" ");
        requests.push({
          time: date[1] + " " + date[2] + " " + date[4],
          response: result.data[key][i][1],
          status_code: result.data[key][i][2],
          method: result.data[key][i][3],
          path: key
        });
      }
    }
    requests.sort((a, b) => {
      return (a.response >= b.response ? -1 : a.response < b.response ? 1 : 0);
    });
    this.selectTopRequests(requests, this.props.topInterval);
  }

  selectTopRequests(requests, topSize){
    if(requests.length < topSize){
      this.setState({top: requests, requests: requests});
      return;
    }
    var topSlow = [];
    for(var i = 0; i < topSize; i++) {
      topSlow.push(requests[i]);
    }
    this.setState({top: topSlow, requests: requests});
  }
  render() {
    return (
      <div>
      <div>
      <h3>
      Top slow: <SelectTopInterval selectTopRequests={this.selectTopRequests} requests={this.state.requests}/>
      </h3>
      </div>
      <TopTable top={this.state.top} />
      </div>
    )
  }
}

TopSlow.defaultProps = {
  from: "1h",
  topInterval: 10
}
