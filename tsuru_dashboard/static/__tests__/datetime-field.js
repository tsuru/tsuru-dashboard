import React from 'react';
import { shallow, mount } from 'enzyme';
import moment from 'moment';

import DateTime from 'react-datetime';
import DateTimeField from '../js/src/components/datetime-field';

describe('DateTimeField', () => {
  it('should render an span as wrapper', () => {
    const dtField = shallow(<DateTimeField/>);
    expect(dtField.is('span')).toBe(true);
  });

  it('should customize the span style', () => {
    const style = {color: 'red'};
    const dtField = shallow(<DateTimeField style={style} />);
    expect(dtField.prop('style')).toEqual(style);
  });

  it('should render a react DateTime component', () => {
    const dtField = shallow(<DateTimeField />);
    expect(dtField.find(DateTime).length).toBe(1);
  });

  it('should have a fixed className', () => {
    const dtField = shallow(<DateTimeField />);
    expect(dtField.find(DateTime).prop('className')).toBe('datetime-field');
  });

  it('should set an initial formatted date value via props', () => {
    const isoDate = '2017-10-31T02:00:00.000Z';
    const dtField = shallow(<DateTimeField value={isoDate} />);
    const expectedDate = moment(isoDate).format('MM/DD/YYYY h:mm A');
    expect(dtField.find(DateTime).prop('value')).toBe(expectedDate);
  });

  it('should customize inputProps.placeholder via props', () => {
    const dtField = shallow(<DateTimeField placeholder='enter some date' />);
    expect(dtField.find(DateTime).prop('inputProps').placeholder).toBe('enter some date');
  });

  it('should have a fixed className for inputProps', () => {
    const dtField = shallow(<DateTimeField />);
    expect(dtField.find(DateTime).prop('inputProps').className).toBe('datetime-field__input');
  });

  it('should render a hidden input to keep iso formatted dates', () => {
    const dtField = shallow(<DateTimeField />);
    expect(dtField.find('input[type="hidden"]').length).toBe(1);
  });

  it('should customize the hidden input name via props', () => {
    const dtField = shallow(<DateTimeField name='datetime_field' />);
    expect(dtField.find('input[type="hidden"]').prop('name')).toBe('datetime_field');
  });

  it('should set an initial iso formatted date value to the hidden input', () => {
    const isoDate = '2017-10-31T02:00:00.000Z';
    const dtField = shallow(<DateTimeField value={isoDate} />);
    expect(dtField.find('input[type="hidden"]').prop('value')).toBe(isoDate);
  });

  it('should set an iso formatted date value to the hidden input on change', () => {
    const selectedDate = moment('2017-10-31 14:00:00-02:00');
    const dtField = shallow(<DateTimeField />);
    const formatedDate = '2017-10-31T16:00:00.000Z';
    dtField.find(DateTime).simulate('change', selectedDate);
    expect(dtField.state('isoValue')).toBe(formatedDate);
    expect(dtField.find('input[type="hidden"]').prop('value')).toBe(formatedDate);
  });

  it('should set a display formatted date value to the DateTime component', () => {
    const selectedDate = moment('2017-10-31 14:00:00-02:00');
    const dtField = shallow(<DateTimeField />);
    const formatedDate = selectedDate.format('MM/DD/YYYY h:mm A');
    dtField.find(DateTime).simulate('change', selectedDate);
    expect(dtField.state('value')).toBe(formatedDate);
    expect(dtField.find(DateTime).prop('value')).toBe(formatedDate);
  });

  it('should set an empty date value to the hidden input for invalid selected dates', () => {
    const dtField =shallow(<DateTimeField />);
    dtField.find(DateTime).simulate('change', '');
    expect(dtField.state('isoValue')).toBe('');
    expect(dtField.find('input[type="hidden"]').prop('value')).toBe('');
  });

  it('should set an empty date value to the DateTime component', () => {
    const dtField = shallow(<DateTimeField />);
    dtField.find(DateTime).simulate('change', '');
    expect(dtField.state('value')).toBe('');
    expect(dtField.find(DateTime).prop('value')).toBe('');
  });
});
