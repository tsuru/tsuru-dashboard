import React from 'react';
import { shallow } from 'enzyme';

import TextInput from '../js/src/components/text-input';
import styles from '../js/src/components/text-input.css.js';

describe('TextInput', () => {
  it('should render an input text element', () => {
    const textInput = shallow(<TextInput/>);
    expect(textInput.is('input[type="text"]')).toBe(true);
  });

  it('should customize the name attr via props', () => {
    const textInput = shallow(<TextInput name='my_input' />);
    expect(textInput.is('[name="my_input"]')).toBe(true);
  });

  it('should customize the placeholder attr via props', () => {
    const textInput = shallow(<TextInput placeholder='enter some input' />);
    expect(textInput.is('[placeholder="enter some input"]')).toBe(true);
  });

  it('should customize the defaultValue via name prop', () => {
    const textInput = shallow(<TextInput value='some value' />);
    expect(textInput.prop('defaultValue')).toBe('some value');
  });

  it('should customize the onChange via props', () => {
    const onChange = jest.fn();
    const textInput = shallow(<TextInput onChange={onChange} />);
    textInput.simulate('change');
    expect(onChange).toBeCalled();
  });

  it('should have some default styles', () => {
    const textInput = shallow(<TextInput />);
    expect(textInput.prop('style')).toEqual(styles.textInput);
  });

  it('should override styles', () => {
    const textInput = shallow(<TextInput style={{borderRadius: '10px'}} />);
    expect(textInput.prop('style').borderRadius).toBe('10px');
  });
});
