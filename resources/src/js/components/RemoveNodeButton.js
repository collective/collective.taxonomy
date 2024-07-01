import React, { PropTypes } from 'react';
import { defineMessages, injectIntl } from 'react-intl';

import Button from './common/Button';

const messages = defineMessages({
  removeNodeLabel: {
    id: 'removeNodeLabel',
    description: 'Remove node button label',
    defaultMessage: 'Remove this node'
  }
});

const RemoveNodeButton = ({ parentId, id, index, intl, removeNode }) => (
  <Button
    handleClick={() => removeNode(parentId, id, index)}
    title={intl.formatMessage(messages.removeNodeLabel)}
  >
    <i className="taxonomy-icon-minus"></i>
  </Button>
);

RemoveNodeButton.propTypes = {
  parentId: PropTypes.string.isRequired,
  id: PropTypes.string.isRequired,
  index: PropTypes.number.isRequired,
  intl: PropTypes.object.isRequired,
  removeNode: PropTypes.func.isRequired
};

export default injectIntl(RemoveNodeButton);
