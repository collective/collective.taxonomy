import { connect } from 'react-redux'

import EditableValues from '../components/EditableValues'

export const mapStateToProps = (
  { languages, selectedLanguage }
) => ({
  selectedLanguage,
  languages: Object.keys(languages),
})

export default connect(
  mapStateToProps
)(EditableValues)
