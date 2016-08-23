import React, { Component } from 'react';
import SwitchButton from 'backstage-switch-button';
import Dropdown from 'backstage-dropdown';
import styles from './event-list.css';


export class EventFilters extends Component {
  constructor(props) {
    super(props);

  }

  render() {
    const options = [
      'admin.create',
      'admin.delete',
      'service-instance.update.grant',
    ];
    return (
      <div id='filter'>
        <form action='' method='GET' ref='form'>
          <Dropdown
            placeholder='choose an event kind'
            options={options}
            style={styles.eventFilter}
            name='kindName'
          />
          <SwitchButton
            label='error only'
            name='errorOnly'
            style={styles.eventFilter}
          />
          <SwitchButton
            label='running only'
            name='running'
            style={styles.eventFilter}
          />
          <button ref='btn' type='submit'>filter</button>
        </form>
      </div>
    );
  }
}
