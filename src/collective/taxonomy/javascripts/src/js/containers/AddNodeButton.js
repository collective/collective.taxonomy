import { connect } from 'react-redux'
import uid from 'uid'

import { addNode } from '../actions'
import AddNodeButton from '../components/AddNodeButton'

export const mapStateToProps = ({ languages }) => ({
  languages
})

export const mapDispatchToProps = (dispatch, { index, parentId }) => ({
  addNode: () => dispatch(addNode(parentId, index, uid(10)))
})

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(AddNodeButton)
