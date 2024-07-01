import React, { PropTypes } from 'react';
import { defineMessages, injectIntl } from 'react-intl';

import Button from './common/Button';

const messages = defineMessages({
  moveDownLabel: {
    id: 'moveDownLabel',
    description: 'Move node down label',
    defaultMessage: 'Move node down'
  }
});

const MoveDownButton = ({ parentId, id, index, intl, moveDown }) => (
  <Button
    handleClick={() => moveDown(parentId, id, index)}
    title={intl.formatMessage(messages.moveDownLabel)}
  >
    <i className="taxonomy-icon-down"></i>
  </Button>
);

MoveDownButton.propTypes = {
  parentId: PropTypes.string.isRequired,
  id: PropTypes.string.isRequired,
  index: PropTypes.number.isRequired,
  intl: PropTypes.object.isRequired,
  moveDown: PropTypes.func.isRequired
};

export default injectIntl(MoveDownButton);
