import React, { PropTypes } from 'react';
import { defineMessages, injectIntl } from 'react-intl';

import Button from './common/Button';

const messages = defineMessages({
  moveUpLabel: {
    id: 'moveUpLabel',
    description: 'Move node up label',
    defaultMessage: 'Move node up'
  }
});

const MoveUpButton = ({ parentId, id, index, intl, moveUp }) => (
  <Button
    handleClick={() => moveUp(parentId, id, index)}
    title={intl.formatMessage(messages.moveUpLabel)}
  >
    <i className="taxonomy-icon-up"></i>
  </Button>
);

MoveUpButton.propTypes = {
  parentId: PropTypes.string.isRequired,
  id: PropTypes.string.isRequired,
  index: PropTypes.number.isRequired,
  intl: PropTypes.object.isRequired,
  moveUp: PropTypes.func.isRequired
};

export default injectIntl(MoveUpButton);
