import React, { PropTypes } from 'react'
import { defineMessages, injectIntl, FormattedMessage } from 'react-intl'

import MessageBox from './common/MessageBox'
import Spinner from './common/Spinner'
import FormControls from './FormControls'
import Tree from '../containers/Tree'
import LanguageSelector from '../containers/LanguageSelector'

const messages = defineMessages({
  changesMade: {
    id: 'changesMade',
    description: 'Changes have been made warning message.',
    defaultMessage: 'Changes have been made but you have to click on submit ' +
                    'button to save these changes.',
  }
})

const App = ({
  dirty,
  intl,
  isPending,
  message,
  saveTree,
  status,
}) => {
  const portalURL = $('base').attr('href')
  return (
    <div>
      { isPending ? <Spinner imageURL={ `${portalURL}/spinner.gif` } /> : null }

      { status ? <MessageBox status={ status } message={ message } /> : null }

      { dirty ? (
        <MessageBox
          status="error"
          message={ intl.formatMessage(messages.changesMade) }
        />) : null }

      <div>
        <h1>
          <FormattedMessage
            id="appTitle"
            description="App title"
            defaultMessage="Edit taxonomy data"
          />
        </h1>
        <LanguageSelector />
        <Tree />
        <FormControls
          dirty={ dirty }
          saveTree={ saveTree }
        />
      </div>
    </div>
  )
}

App.propTypes = {
  dirty: PropTypes.bool.isRequired,
  intl: PropTypes.object.isRequired,
  isPending: PropTypes.bool.isRequired,
  message: PropTypes.string.isRequired,
  saveTree: PropTypes.func.isRequired,
  status: PropTypes.string.isRequired,
}

export default injectIntl(App)
