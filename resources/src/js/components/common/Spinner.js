import React, { PropTypes } from 'react';

const Spinner = ({ imageURL }) => (
  <div id="ajax-spinner" style={{ display: 'block' }}>
    <img src={imageURL} alt="" />
  </div>
);

Spinner.propTypes = {
  imageURL: PropTypes.string.isRequired
};

export default Spinner;
