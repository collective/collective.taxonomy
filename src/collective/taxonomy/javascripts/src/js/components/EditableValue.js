import React, { PropTypes } from 'react'
import ReactPencil from 'react-pencil'

const EditableValue = ({
  editTranslation,
  hidden,
  id,
  language,
  value,
}) => (
  <span>
    { hidden ? null : (
      <ReactPencil
        language={ language }
        name={ `${id}-${language}` }
        value={ value }
        placeholder="Insert value here"
        pencil
        onEditDone={ (name, newValue) => editTranslation(id, language, newValue) }
      />)
    }
  </span>
)

EditableValue.propTypes = {
  editTranslation: PropTypes.func.isRequired,
  hidden: PropTypes.bool,
  id: PropTypes.string.isRequired,
  language: PropTypes.string.isRequired,
  value: PropTypes.string,
}

EditableValue.defaultProps = {
  hidden: false
}

export default EditableValue
