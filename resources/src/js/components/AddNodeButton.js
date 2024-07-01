import React, { PropTypes } from 'react';
import { defineMessages, injectIntl } from 'react-intl';

import Button from './common/Button';

const messages = defineMessages({
  addNodeLabel: {
    id: 'addNodeLabel',
    description: 'Add node button label',
    defaultMessage: 'Add a node at the same level'
  }
});

const AddNodeButton = ({ addNode, children, intl, title }) => (
  <Button
    handleClick={addNode}
    title={title || intl.formatMessage(messages.addNodeLabel)}
  >
    {children || <i className="taxonomy-icon-plus"></i>}
  </Button>
);

AddNodeButton.propTypes = {
  children: React.PropTypes.oneOfType([
    React.PropTypes.array,
    React.PropTypes.element,
    React.PropTypes.string
  ]),
  intl: PropTypes.object.isRequired,
  title: PropTypes.string,
  addNode: PropTypes.func.isRequired
};

export default injectIntl(AddNodeButton);
