import React, { Component } from 'react';
import styles from './text-input.css.js';

const TextInput = (props) => {
  return (
    <input type="text"
      name={props.name}
      placeholder={props.placeholder}
      defaultValue={props.value}
      style={Object.assign({}, props.style || {}, styles.textInput)}
      onChange={props.onChange}
    />
  );
}

export default TextInput;