var React = require('react'),
    fuzzy = require('fuzzy');

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
    var appNodes = this.props.data.map(function(app) {
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
    return {cached: [], apps: []};
  },
  loadApps: function() {
    var that = this;
    var request = new XMLHttpRequest();
    request.open('GET', this.props.url);

    request.onload = function() {
      if (request.status >= 200 && request.status < 400) {
        var data = JSON.parse(request.responseText);
        that.setState({cached: data.apps, apps: data.apps});
      }
    };
    request.send()
  },
  appsByName: function(name) {
    if (this.state.cached.length == 0 ) {
      this.loadApps();
      return;
    } 
    var options = {
      extract: function(el) { return el.name }
    };
    var results = fuzzy.filter(name, this.state.cached, options);
    this.setState({apps: results.map(function(el) { return el.original; })});
  },
  componentDidMount: function() {
    this.appsByName("");
  },
  render: function() {
    return (
      <div className="app-list">
        <AppSearch onSearchSubmit={this.appsByName} />
        <AppTable data={this.state.apps} />
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
