import { connect } from 'react-redux'

import { removeNode } from '../actions'
import RemoveNodeButton from '../components/RemoveNodeButton'

export default connect(
  null,
  { removeNode }
)(RemoveNodeButton)
