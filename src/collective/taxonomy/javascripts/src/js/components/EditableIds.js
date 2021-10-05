import React, { PropTypes } from 'react';

import EditableId from '../containers/EditableId';

const EditableIds = ({ id, selectedLanguage, languages }) => (
  <div style={{ display: 'inline' }}>
    {languages.map(language => (
      <EditableId
        key={`${id}-${language}`}
        id={id}
        language={language}
        hidden={language !== selectedLanguage}
      />
    ))}
  </div>
);

EditableIds.propTypes = {
  id: PropTypes.string.isRequired,
  languages: PropTypes.array.isRequired,
  selectedLanguage: PropTypes.string.isRequired
};

export default EditableIds;
