var React = require('react');

var SelectTopInterval = React.createClass({
  handleChange: function(e) {
    e.preventDefault();
    var topSize = e.target.value.trim();
    this.props.selectTopRequests(this.props.requests, topSize);
  },
  render: function() {
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
});

var RequestRow = React.createClass({
  render: function() {
    return (
      <tr>
        <td>{this.props.request.method}</td>
        <td>{this.props.request.path}</td>
        <td>{this.props.request.status_code}</td>
        <td>{this.props.request.response}</td>
        <td>{this.props.request.time}</td>
      </tr>
    );
  }
});

var TopTable = React.createClass({
  render: function() {
    var topNodes = this.props.top.map(function(result) {
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
          {topNodes}
        </tbody>
      </table>
    );
  }

});

var TopSlow = React.createClass({
  getDefaultProps: function() {
    return {
      from: "1h",
      topInterval: 10,
    }
  },
  getInitialState: function() {
    return {top: [], requests: []};
  },
  componentDidMount: function() {
    this.loadData();
  },
  loadData: function() {
    var appName = this.props.appName;
    var kind = this.props.kind;
    var from = this.props.from;
    var url ="/metrics/" + appName + "/?metric=" + kind + "&date_range=" + from;
    $.getJSON(url, function(data) {
      if (Object.keys(data.data).length === 0)
        data.data = {" ": [1,1]};
        this.sortData(data);
    }.bind(this));
  },
  sortData: function(result) {
    var requests = [];
    for(key in result.data) {
      for(i in result.data[key]){
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
    requests.sort(function(a,b){
      return (a.response >= b.response ? -1 : a.response < b.response ? 1 : 0);
    });
    this.selectTopRequests(requests, this.props.topInterval);
  },
  selectTopRequests: function(requests, topSize){
    if(requests.length < topSize){
      this.setState({top: requests, requests: requests});
      return;
    }
    var topSlow = [];
    for(var i = 0; i < topSize; i++) {
      topSlow.push(requests[i]);
    }
    this.setState({top: topSlow, requests: requests});
  },
  render: function() {
    return (
      <div>
        <div>
          <h3>
            Top slow: <SelectTopInterval selectTopRequests={this.selectTopRequests} requests={this.state.requests}/>
          </h3>
        </div>
        <TopTable top={this.state.top} />
      </div>
    );
  }
});

module.exports = {
    TopSlow: TopSlow,
};