var React = require('react');

var AppSearch = React.createClass({
  handleSubmit: function(e) {
    var name = e.target.value.trim();
    if (!name) {
      return;
    }
    this.props.onSearchSubmit(name);
  },
  render: function() {
    return (
      <div className="search">
        <form onChange={this.handleSubmit}>
          <input type="text" ref="name" placeholder="search apps by name" />
        </form>
      </div>
    );
  }
});

var App = React.createClass({
  render: function() {
    return (
      <tr>
        <td>
          <a href={this.props.name} title="App Details">
            {this.props.name}
          </a>
        </td>
      </tr>
    );
  }
});

var AppTable = React.createClass({
  render: function() {
    var appNodes = this.props.data.apps.map(function(app) {
      return (
        <App name={app.name} url={app.url}/>
      );
    });
    return (
	  <table className="table">
        {appNodes}
	  </table>
    );
  }
});

var AppList = React.createClass({
  getInitialState: function() {
    return {data: {apps: []}};
  },
  loadCommentsFromServer: function(name) {
    var that = this;
    var request = new XMLHttpRequest();
    request.open('GET', this.props.url + "?name=" + name, true);

    request.onload = function() {
      if (request.status >= 200 && request.status < 400) {
        var data = JSON.parse(request.responseText);
        that.setState({data: data});
      }
    };

    request.send()
  },
  componentDidMount: function() {
    this.loadCommentsFromServer("");
  },
  handleSearchSubmit: function(name) {
    this.loadCommentsFromServer(name);
  },
  render: function() {
    return (
      <div className="app-list">
        <AppSearch onSearchSubmit={this.handleSearchSubmit} />
        <AppTable data={this.state.data} />
      </div>
    );
  }
});

var List = {
    AppSearch: AppSearch,
    AppList: AppList,
    AppTable: AppTable,
    App: App
}

module.exports = List;
