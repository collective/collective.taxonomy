import React, { Component, PropTypes } from 'react';
import { defineMessages, injectIntl } from 'react-intl';

const messages = defineMessages({
  backToSettingsLabel: {
    id: 'backToSettingsLabel',
    description: 'Back to settings button label.',
    defaultMessage: 'Back to settings'
  },
  submitLabel: {
    id: 'submitLabel',
    description: 'Submit button label.',
    defaultMessage: 'Submit'
  }
});

class FormControls extends Component {
  static propTypes = {
    dirty: PropTypes.bool.isRequired,
    duplicated: PropTypes.bool.isRequired,
    intl: PropTypes.object.isRequired,
    saveTree: PropTypes.func.isRequired
  };

  constructor() {
    super();
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(e) {
    e.preventDefault();
    this.props.saveTree();
  }

  handleBack(e) {
    e.preventDefault();
    const baseUrl = $('base').attr('href') || $('body').attr('data-portal-url');
    window.location.href = `${baseUrl}/@@taxonomy-settings`;
  }

  render() {
    const { dirty, duplicated, intl } = this.props;
    return (
      <div className="formControls">
        <input
          id="form-buttons-save"
          className="btn btn-primary"
          type="submit"
          value={intl.formatMessage(messages.submitLabel)}
          disabled={!dirty ? 'disabled' : null}
          onClick={this.handleClick}
        />
        &nbsp;
        <input
          id="form-buttons-cancel"
          className="btn btn-secondary"
          onClick={this.handleBack}
          type="submit"
          value={intl.formatMessage(messages.backToSettingsLabel)}
        />
      </div>
    );
  }
}

export default injectIntl(FormControls);
