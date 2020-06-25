import React, { PropTypes } from 'react';
import { defineMessages, injectIntl } from 'react-intl';

import AddNodeButton from '../containers/AddNodeButton';
import EditableValues from '../containers/EditableValues';
import RemoveNodeButton from '../containers/RemoveNodeButton';
import MoveDownButton from '../containers/MoveDownButton';
import MoveUpButton from '../containers/MoveUpButton';

const messages = defineMessages({
  addChildNodeLabel: {
    id: 'addChildNodeLabel',
    description: 'Add a child node button label',
    defaultMessage: 'Add a term inside this node'
  }
});

const Leaf = ({ id, index, intl, language, parentId, title }) => (
  <div className="info">
    <EditableValues id={id} selectedLanguage={language} />
    &nbsp;&nbsp;&nbsp;
    <AddNodeButton index={index} parentId={parentId} />
    &nbsp;
    <RemoveNodeButton id={id} index={index} parentId={parentId} title={title} />
    &nbsp;
    <AddNodeButton
      index={index}
      parentId={id}
      title={intl.formatMessage(messages.addChildNodeLabel)}
    >
      <i className="taxonomy-icon-flow-split"></i>
    </AddNodeButton>
    <MoveDownButton id={id} index={index} parentId={parentId} />
    <MoveUpButton id={id} index={index} parentId={parentId} />
  </div>
);

Leaf.propTypes = {
  id: PropTypes.string.isRequired,
  index: PropTypes.number.isRequired,
  intl: PropTypes.object.isRequired,
  language: PropTypes.string.isRequired,
  parentId: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired
};

export default injectIntl(Leaf);
