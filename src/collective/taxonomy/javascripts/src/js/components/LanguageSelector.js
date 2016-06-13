import React, { PropTypes } from 'react'
import { FormattedMessage } from 'react-intl'

const LanguageSelector = ({ languages, selectLanguage, selectedLanguage }) => (
  <p>
    <label>
      <FormattedMessage
        id="languageSelectorLabel"
        description="Message that invites the user to select a message"
        defaultMessage="Select the language to edit: "
      />
    </label>&nbsp;
    <select
      value={ selectedLanguage }
      onChange={ (e) => selectLanguage(e.target.value) }
    >
      { Object.keys(languages).map(
        lang => <option key={ lang } value={ lang }>{ languages[lang] }</option>)
      }
    </select>
  </p>
)

LanguageSelector.propTypes = {
  languages: PropTypes.object.isRequired,
  selectLanguage: PropTypes.func.isRequired,
  selectedLanguage: PropTypes.string.isRequired,
}

export default LanguageSelector
