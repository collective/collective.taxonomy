import React, { PropTypes } from 'react';
import ReactPencil from 'react-pencil';
import { defineMessages, injectIntl } from 'react-intl';

const messages = defineMessages({
  editIdentifierLabel: {
    id: 'editIdentifierLabel',
    description: 'Edit identifier',
    defaultMessage: 'Edit node identifier'
  }
});

class CustomReactPencil extends ReactPencil {
  renderPencilButton() {
    return ((
      <button className="pencil-button" onClick={() => this.focus()}>
        <i className="taxonomy-icon-pencil"></i>
      </button>
    ): null);
  }
}

const EditableId = ({
  editIdentifier,
  hidden,
  id,
  index,
  parentId,
  intl,
  language
}) => (
  <span>
    {hidden ? null : (
      <CustomReactPencil
        language={language}
        name={`${id}`}
        value={`${id}`}
        className="identifier-input"
        placeholder={intl.formatMessage(messages.editIdentifierLabel)}
        pencil
        onEditDone={(name, newValue) =>
          editIdentifier(id, index, parentId, language, newValue)
        }
      />
    )}
  </span>
);

EditableId.propTypes = {
  editIdentifier: PropTypes.func.isRequired,
  hidden: PropTypes.bool,
  id: PropTypes.string.isRequired,
  index: PropTypes.number.isRequired,
  parentId: PropTypes.string.isRequired,
  intl: PropTypes.object.isRequired,
  language: PropTypes.string.isRequired
};

EditableId.defaultProps = {
  hidden: false
};

export default injectIntl(EditableId);
