import React, { Component, PropTypes } from 'react';
import { defineMessages, injectIntl, FormattedMessage } from 'react-intl';

import MessageBox from './common/MessageBox';
import Spinner from './common/Spinner';
import FormControls from './FormControls';
import HideTreeCheckbox from './HideTreeCheckbox';
import TaxonomyTree from './TaxonomyTree';

const messages = defineMessages({
  changesMade: {
    id: 'changesMade',
    description: 'Changes have been made warning message.',
    defaultMessage:
      'Changes have been made but you have to click on submit ' +
      'button to save these changes.'
  }
});

class App extends Component {
  constructor() {
    super();
    this.state = {
      viewTreeShown: false
    };
    this.handleToggleViewTree = this.handleToggleViewTree.bind(this);
  }

  handleToggleViewTree() {
    this.setState({
      viewTreeShown: !this.state.viewTreeShown
    });
  }

  render() {
    const {
      defaultLanguage,
      dirty,
      intl,
      isPending,
      message,
      saveTree,
      status
    } = this.props;
    const portalURL =
      $('base').attr('href') || $('body').attr('data-portal-url');
    return (
      <div>
        {isPending ? <Spinner imageURL={`${portalURL}/spinner.gif`} /> : null}

        {status ? <MessageBox status={status} message={message} /> : null}

        {dirty ? (
          <MessageBox
            status="error"
            message={intl.formatMessage(messages.changesMade)}
          />
        ) : null}

        <div>
          <h1>
            <FormattedMessage
              id="appTitle"
              description="App title"
              defaultMessage="Edit taxonomy data"
            />
          </h1>

          <HideTreeCheckbox
            checked={this.state.viewTreeShown}
            onChange={this.handleToggleViewTree}
          />

          <TaxonomyTree defaultLanguage={defaultLanguage} />

          {this.state.viewTreeShown ? (
            <TaxonomyTree defaultLanguage={defaultLanguage} editable={false} />
          ) : null}

          <div style={{ clear: 'both' }} />

          <FormControls dirty={dirty} saveTree={saveTree} />
        </div>
      </div>
    );
  }
}

App.propTypes = {
  defaultLanguage: PropTypes.string.isRequired,
  dirty: PropTypes.bool.isRequired,
  intl: PropTypes.object.isRequired,
  isPending: PropTypes.bool.isRequired,
  message: PropTypes.string.isRequired,
  saveTree: PropTypes.func.isRequired,
  status: PropTypes.string.isRequired
};

export default injectIntl(App);
