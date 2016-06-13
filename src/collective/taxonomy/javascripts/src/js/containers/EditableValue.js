import { connect } from 'react-redux'

import { editTranslation } from '../actions'
import EditableValue from '../components/EditableValue'

export const mapStateToProps = (
  { tree: { nodes } },
  { id, language }
) => ({
  value: nodes[id].translations[language]
})

export default connect(
  mapStateToProps,
  { editTranslation }
)(EditableValue)
