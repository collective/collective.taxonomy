import { connect } from 'react-redux'

import { saveTree } from '../actions'
import App from '../components/App'

const mapStateToProps = ({
  tree: { dirty },
  saveTree: { isPending, message, status },
}) => ({
  dirty,
  isPending,
  message,
  status,
})

export default connect(
  mapStateToProps,
  { saveTree }
)(App)
