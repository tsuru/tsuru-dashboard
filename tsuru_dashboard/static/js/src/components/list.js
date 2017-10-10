import React, { Component } from "react";
import fuzzy from "fuzzy";
import { Loading } from "./loading";

if(typeof window.jQuery === 'undefined') {
  var $ = require('jquery');
} else {
  var $ = window.jQuery;
}

export class AppSearch extends Component {
  constructor(props) {
    super(props);

    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(e) {
    e.preventDefault();
    var name = e.target.value.trim();
    this.props.search(name);
  }

  render() {
    return (
      <div className="search">
      <input type="text"
      ref="name"
      placeholder="search apps by name"
      onChange={this.handleChange} />
      <AppAdd />
      <div className="clearfix"></div>
      </div>
    )
  }
}

class AppAdd extends Component {
  render() {
    return (
      <a title="new app" href="/apps/create/"><i className="icono-plus"></i></a>
    )
  }
}

export class App extends Component {
  render() {
    return (
      <tr>
      <td>
      <a href={this.props.name} title="App Details">
      {this.props.name}
      </a>
      </td>
      </tr>
    )
  }
}

export class AppTable extends Component {
  render() {
    var appNodes = this.props.data.map((app) => {
      return (
        <App key={app.name} name={app.name} url={app.url}/>
      );
    });
    return (
      <table className="table">
      <tbody>{appNodes}</tbody>
      </table>
    )
  }
}

export class AppList extends Component {
  constructor(props) {
    super(props);

    this.state = {
      cached: [],
      apps: [],
      loading: false,
      term: ""
    }

    this.appsByName = this.appsByName.bind(this);
  }

  loadApps() {
    this.setState({loading: true});
    $.ajax({
      type: 'GET',
      url: this.props.url,
      success: (data) => {
        this.setState({cached: data.apps, apps: data.apps, loading: false});

        if (this.state.term.length > 0) {
          this.appsByName(this.state.term);
          this.setState({term: ''});
        }

      }
    });
  }

  appsByName(name) {
    if (this.state.loading) {
      this.setState({term: name});
      return;
    }

    if (this.state.cached.length == 0 ) {
      this.loadApps();
      return;
    }
    var options = {
      extract: (el) => { return el.name }
    };
    var results = fuzzy.filter(name, this.state.cached, options);
    this.setState({apps: results.map((el) => { return el.original; })});
  }

  componentDidMount() {
    this.appsByName("");
  }

  render() {
    return (
      <div className="app-list">
      <AppSearch search={this.appsByName} />
      {this.state.loading ? <Loading /> : ''}
      <AppTable data={this.state.apps} />
      </div>
    );
  }
}
