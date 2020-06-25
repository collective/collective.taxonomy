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

const EditableValue = ({
  editTranslation,
  hidden,
  id,
  intl,
  language,
  value
}) => (
  <span>
    {hidden ? null : (
      <CustomReactPencil
        language={language}
        name={`${id}-${language}`}
        value={value}
        placeholder={intl.formatMessage(messages.emptyNodePlaceholder)}
        pencil
        onEditDone={(name, newValue) => editTranslation(id, language, newValue)}
      />
    )}
  </span>
);

EditableValue.propTypes = {
  editTranslation: PropTypes.func.isRequired,
  hidden: PropTypes.bool,
  id: PropTypes.string.isRequired,
  intl: PropTypes.object.isRequired,
  language: PropTypes.string.isRequired,
  value: PropTypes.string
};

EditableValue.defaultProps = {
  hidden: false
};

export default injectIntl(EditableValue);
