import { connect } from 'react-redux'

import { selectLanguage } from '../actions'
import LanguageSelector from '../components/LanguageSelector'

export const mapStateToProps = ({
  defaultLanguage,
  languages,
  selectedLanguage
}) => ({
  defaultLanguage,
  languages,
  selectedLanguage,
})

export default connect(
  mapStateToProps,
  { selectLanguage },
)(LanguageSelector)
