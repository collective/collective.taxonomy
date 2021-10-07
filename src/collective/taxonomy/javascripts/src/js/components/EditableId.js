import React, { PropTypes } from 'react';
import ReactPencil from 'react-pencil';
import { defineMessages, injectIntl } from 'react-intl';

const messages = defineMessages({
  emptyNodePlaceholder: {
    id: 'emptyNodePlaceholder',
    description: 'Placeholder for new nodes',
    defaultMessage: 'Insert value here'
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
        placeholder={intl.formatMessage(messages.emptyNodePlaceholder)}
        pencil
        onEditDone={(name, newValue) => editIdentifier(id, index, parentId, language, newValue)}
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
