import React, { PropTypes } from 'react';
import { FormattedMessage } from 'react-intl';

const LanguageSelector = ({ languages, onChange, selectedLanguage }) => (
  <p>
    <label>
      <FormattedMessage
        id="languageSelectorLabel"
        description="Message that invites the user to select a message"
        defaultMessage="Select the language: "
      />
    </label>
    &nbsp;
    <select value={selectedLanguage} onChange={onChange}>
      {Object.keys(languages).map(lang => (
        <option key={lang} value={lang}>
          {languages[lang]}
        </option>
      ))}
    </select>
  </p>
);

LanguageSelector.propTypes = {
  languages: PropTypes.object.isRequired,
  onChange: PropTypes.func.isRequired,
  selectedLanguage: PropTypes.string.isRequired
};

export default LanguageSelector;
