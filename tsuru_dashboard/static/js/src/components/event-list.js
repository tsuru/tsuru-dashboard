import React, { Component } from 'react';
import SwitchButton from 'backstage-switch-button';
import Dropdown from 'backstage-dropdown';
import TextInput from './text-input';
import DateTimeField from './datetime-field';
import styles from './event-list.css';


export class EventFilters extends Component {
  constructor(props) {
    super(props);

    this.state = { options: [] };
  }

  componentDidMount() {
    this.loadKinds();
  }

  loadKinds() {
    $.ajax({
      type: 'GET',
      url: "/events/kinds/",
      success: (data) => {
        let options = [];
        data.forEach((item) => {
          options.push(item.Name);
        });
        this.setState({ options: options });
      }
    });
  }

  render() {
    return (
      <div id='filter'>
        <form action='' method='GET' ref='form'>
          <div style={styles.eventFilterRow}>
            <Dropdown
              placeholder='choose an event kind'
              options={this.state.options}
              style={styles.eventFilter}
              name='kindName'
              value={this.props.kind}
            />
            <SwitchButton
              label='error only'
              name='errorOnly'
              style={styles.eventFilter}
              checked={this.props.errorOnly}
            />
            <SwitchButton
              label='running only'
              name='running'
              style={styles.eventFilter}
              checked={this.props.running}
            />
            <SwitchButton
              label='include removed'
              name='includeRemoved'
              style={styles.eventFilter}
              checked={this.props.includeRemoved}
            />
          </div>
          <div style={styles.eventFilterRow}>
            <TextInput
              placeholder='target name'
              name='target.value'
              value={this.props.target}
              style={styles.eventFilter}
            />
            <TextInput
              placeholder='owner e-mail'
              name='ownerName'
              value={this.props.owner}
              style={styles.eventFilter}
            />
            <DateTimeField
              placeholder='from date'
              name='since'
              value={this.props.since}
              style={styles.eventFilter}
            />
            <DateTimeField
              placeholder='until date'
              name='until'
              value={this.props.until}
              style={styles.eventFilter}
            />
          </div>
          <button ref='btn' type='submit'>filter</button>
        </form>
      </div>
    );
  }
}
