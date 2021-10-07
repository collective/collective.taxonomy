import React, { PropTypes } from 'react';

import EditableId from '../containers/EditableId';

const EditableIds = ({ id, index, parentId, selectedLanguage, languages }) => (
  <div style={{ display: 'inline' }}>
    {languages.map(language => (
      <EditableId
        key={`${id}-${language}`}
        id={id}
        language={language}
        hidden={language !== selectedLanguage}
        index={index}
        parentId={parentId}
      />
    ))}
  </div>
);

EditableIds.propTypes = {
  id: PropTypes.string.isRequired,
  index: PropTypes.number.isRequired,
  parentId: PropTypes.string.isRequired,
  languages: PropTypes.array.isRequired,
  selectedLanguage: PropTypes.string.isRequired
};

export default EditableIds;
