import { connect } from 'react-redux'

import SubTree from '../components/SubTree'
import { editTranslation } from '../actions'

const mapStateToProps = (
  {
    selectedLanguage,
    tree: { nodes },
  },
  { id }
) => {
  const node = nodes[id]
  return {
    selectedLanguage,
    subnodes: node.subnodes,
    title: node.translations[selectedLanguage],
  }
}

export default connect(
  mapStateToProps,
  { editTranslation }
)(SubTree)
