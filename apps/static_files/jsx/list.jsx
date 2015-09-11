var React = require('react');

var AppSearch = React.createClass({
  handleSubmit: function(e) {
    e.preventDefault();
    var name = React.findDOMNode(this.refs.name).value.trim();
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
          <a href="{this.props.url}" title="App Details">
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
    $.ajax({
      url: this.props.url + "?name=" + name,
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
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

React.render(
  <AppList url="/apps/list.json" />,
  document.getElementById('list-container')
);
