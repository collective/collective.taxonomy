import React, { PropTypes } from 'react'

const LanguageSelector = ({ languages, selectLanguage, selectedLanguage }) => (
  <p>
    <label>Select the language to edit: </label>&nbsp;
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
