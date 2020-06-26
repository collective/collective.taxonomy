import React, { PropTypes } from 'react';

import EditableValue from '../containers/EditableValue';

const EditableValues = ({ id, selectedLanguage, languages }) => (
  <div style={{ display: 'inline' }}>
    {languages.map(language => (
      <EditableValue
        key={`${id}-${language}`}
        id={id}
        language={language}
        hidden={language !== selectedLanguage}
      />
    ))}
  </div>
);

EditableValues.propTypes = {
  id: PropTypes.string.isRequired,
  languages: PropTypes.array.isRequired,
  selectedLanguage: PropTypes.string.isRequired
};

export default EditableValues;
