var React = require('react'),
    fuzzy = require('fuzzy'),
    Loading = require('./loading.jsx'),
	$ = require('jquery'),
    PureRenderMixin = require('react-addons-pure-render-mixin');


var AppSearch = React.createClass({
  mixins: [PureRenderMixin],
  handleChange: function(e) {
    e.preventDefault();
    var name = e.target.value.trim();
    this.props.search(name);
  },
  render: function() {
    return (
      <div className="search">
        <input type="text"
               ref="name"
               placeholder="search apps by name"
               onChange={this.handleChange} />
		<AppAdd />
        <div className="clearfix"></div>
      </div>
    );
  }
});

var AppAdd = React.createClass({
  mixins: [PureRenderMixin],
  render: function() {
    return (
	  <a title="new app" href="/apps/create/"><i className="icono-plus"></i></a>
    );
  }
});

var AppStatus = React.createClass({
  getStatus: function() {
    var status = "Stopped";
    if (this.props.units) {
      for (var i = 0; i < this.props.units.length; i++) {
        var unit = this.props.units[i];
        if (unit.Status === "Started") {
          status = "Started";
          break;
        }
        status = unit.Status;
      }
    }
    return status.toLowerCase();
  },
  render: function() {
    var status = this.getStatus();
    return (
	  <img src={"/static/img/" + status + ".svg"} alt={status} title={status} className="app-status"/>
    );
  }
});

var App = React.createClass({
  mixins: [PureRenderMixin],
  render: function() {
    return (
      <tr>
        <td>
          <AppStatus units={this.props.units}/>
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
        <App key={app.name} name={app.name} url={app.url} units={app.units}/>
      );
    });
    return (
	  <table className="table">
        <tbody>{appNodes}</tbody>
	  </table>
    );
  }
});

var AppList = React.createClass({
  getInitialState: function() {
    return {cached: [], apps: [], loading: false, term: ""};
  },
  loadApps: function() {
    this.setState({loading: true});
	$.ajax({
	  type: 'GET',
	  url: this.props.url,
	  success: function(data) {
        this.setState({cached: data.apps, apps: data.apps, loading: false});

        if (this.state.term.length > 0) {
          this.appsByName(this.state.term);
          this.setState({term: ''});
        }

	  }.bind(this)
	});
  },
  appsByName: function(name) {
    if (this.state.loading) {
        this.setState({term: name});    
        return;
    }

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
        <AppSearch search={this.appsByName} />
        {this.state.loading ? <Loading /> : ''}
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
