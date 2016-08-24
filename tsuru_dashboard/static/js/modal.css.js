(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = {
  container: {
    display: 'inline-block',
    height: '32px',
    cursor: 'default'
  },
  modal: {
    width: '465px',
    borderRadius: '4px',
    backgroundColor: '#fff',
    boxShadow: '0 2px 4px 0 rgba(0, 0, 0, 0.3)',
    border: 'solid 1px #ccc',
    display: 'inline-block',
    textAlign: 'left',
    position: 'absolute',
    zIndex: 1000,
    marginLeft: '-232px'
  },
  header: {
    borderBottom: 'solid 2px #ccc',
    padding: '24px'
  },
  body: {
    padding: '24px'
  },
  title: {
    fontFamily: 'Open Sans',
    fontSize: '20px',
    letterSpacing: '-0.8px',
    color: '#333'
  },
  close: {
    color: '#999',
    fontSize: '16px',
    fontWeight: 'bold',
    textAlign: 'center',
    position: 'absolute',
    right: '20px'
  },
  hidden: {
    visibility: 'hidden'
  }
};


},{}]},{},[1]);
