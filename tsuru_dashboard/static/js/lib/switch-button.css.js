(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = {
  container: {
    position: 'relative',
    lineHeight: '100%',
    display: 'inline-block',
    verticalAlign: 'middle',
    margin: 0,
    boxSizing: 'border-box'
  },
  background: {
    cursor: 'pointer',
    marginLeft: '6px',
    display: 'inline-block',
    position: 'relative',
    margin: 0,
    outline: 'none',
    userSelect: 'none',
    boxSizing: 'border-box',
    padding: '2px',
    width: '28px',
    height: '16px',
    backgroundColor: '#999',
    verticalAlign: 'middle',
    borderRadius: '24px',
    transition: 'background 0.4s'
  },
  backgroundHover: {
    backgroundColor: '#666'
  },
  backgroundChecked: {
    backgroundColor: '#0669de'
  },
  backgroundHoverAndChecked: {
    backgroundColor: '#044cb3'
  },
  button: {
    display: 'inline-block',
    position: 'absolute',
    content: '',
    top: '2px',
    left: '2px',
    bottom: '2px',
    width: '12px',
    backgroundColor: '#fff',
    borderRadius: '12px',
    transition: 'margin 0.4s, background 0.4s'
  },
  buttonChecked: {
    marginLeft: '12px'
  },
  checkbox: {
    position: 'absolute',
    marginLeft: '-9999px',
    visibility: 'hidden'
  },
  label: {
    height: '16px',
    fontSize: '14px',
    fontFamily: 'Open Sans',
    lineHeight: '1.1',
    letterSpacing: '-0.2px',
    color: '#666',
    marginLeft: '8px'
  }
};


},{}]},{},[1]);
