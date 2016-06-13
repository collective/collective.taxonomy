import React, { PropTypes } from 'react'

import MessageBox from './common/MessageBox'
import Spinner from './common/Spinner'
import FormControls from './FormControls'
import Tree from '../containers/Tree'
import LanguageSelector from '../containers/LanguageSelector'

const App = ({
  dirty,
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
          message="Changes have been made but you have to click on submit button to save these changes."
        />) : null }

      <div>
        <h1>Edit taxonomy data</h1>
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
  isPending: PropTypes.bool.isRequired,
  message: PropTypes.string.isRequired,
  saveTree: PropTypes.func.isRequired,
  status: PropTypes.string.isRequired,
}

export default App
