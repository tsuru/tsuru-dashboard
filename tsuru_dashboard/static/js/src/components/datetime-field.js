import React, { Component } from 'react';
import DateTime from 'react-datetime';
import moment from 'moment';

export default class DateTimeField extends Component {
  constructor(props) {
    super(props);

    this.state = {
      value: this.isoToDisplay(props.value),
      isoValue: props.value
    };
  }

  isoToDisplay(date) {
    const momentDate = moment(date);
    if (momentDate.isValid()) {
      return momentDate.format('MM/DD/YYYY h:mm A');
    }
  }

  onPick(date) {
    if (date && date.isValid()) {
      this.setState({
        value: this.isoToDisplay(date),
        isoValue: date.toISOString()
      });
    } else {
      this.setState({ value: '', isoValue: '' });
    }
  }

  render() {
    return (
      <span style={Object.assign({}, this.props.style || {})}>
        <DateTime
          className='datetime-field'
          value={this.state.value}
          inputProps={{
            placeholder: this.props.placeholder,
            className: 'datetime-field__input'
          }}
          onChange={this.onPick.bind(this)}
        />
        <input
          type='hidden'
          name={this.props.name}
          value={this.state.isoValue}
        />
      </span>
    );
  }

}