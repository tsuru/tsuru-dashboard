import React from "react";
import { Loading } from "./loading";
import { Metrics } from "../components/metrics";

if(typeof window.jQuery === 'undefined') {
  var $ = require('jquery');
} else {
  var $ = window.jQuery;
}

export class ComponentList extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      components: [],
      loading: false
    }
  }

  componentDidMount() {
    this.setState({loading: true});
    $.ajax({
      type: 'GET',
      url: this.props.url,
      success: (data) => {
        this.setState({components: data.components, loading: false});
      }
    });
  }

  render() {
    return (
      <div className="component-list">
        {this.state.loading ? <Loading /> : ''}
        {this.state.components.map((component) => {
          return (<Component name={component} key={component}/>);
        })}
      </div>
    )
  }
}

export class Component extends React.Component {
  render() {
    var metrics = ["cpu_max", "mem_max", "swap", "connections", "units", "nettx", "netrx"];
    return (
      <div className='component'>
        <h2>{this.props.name}</h2>
        <div className='metrics'>
          <Metrics targetName={this.props.name} targetType={"component"} metrics={metrics} />
        </div>
      </div>
    );
  }
}
