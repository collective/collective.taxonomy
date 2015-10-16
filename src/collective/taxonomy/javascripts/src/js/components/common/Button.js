import React, { Component, PropTypes } from 'react'


export default class Button extends Component {

  static propTypes = {
    children: React.PropTypes.oneOfType([
      React.PropTypes.array,
      React.PropTypes.element,
      React.PropTypes.string]).isRequired,
    handleClick: PropTypes.func,
    title: PropTypes.string
  }

  render() {
    const { children, handleClick, title, ...other } = this.props
    return (
        <button title={ title || null } onClick={ handleClick || null }>
          { children }
        </button>
      )
  }

}
