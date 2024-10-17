import React, { PropTypes } from 'react';

const Button = ({ children, handleClick, title }) => (
  <button
    title={title}
    onClick={handleClick}
    style={{ display: 'inline-block' }}
  >
    {children}
  </button>
);

Button.propTypes = {
  children: React.PropTypes.oneOfType([
    React.PropTypes.array,
    React.PropTypes.element,
    React.PropTypes.string
  ]).isRequired,
  handleClick: PropTypes.func,
  title: PropTypes.string.isRequired
};

export default Button;
