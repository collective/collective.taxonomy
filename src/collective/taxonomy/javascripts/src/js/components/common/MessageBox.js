import React, { PropTypes } from 'react';

const MessageBox = ({ message, status }) => (
  <dl
    className={`portalMessage ${status} alert alert-${
      status === 'error' ? 'danger' : status
    }`}
  >
    <dt>{status}</dt>
    <dd>{message}</dd>
  </dl>
);

MessageBox.propTypes = {
  message: PropTypes.string.isRequired,
  status: PropTypes.string.isRequired
};

export default MessageBox;
