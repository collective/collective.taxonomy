import { connect } from 'react-redux';

import { saveTree } from '../actions';
import App from '../components/App';

const mapStateToProps = ({
  defaultLanguage,
  tree: { dirty, duplicated, duplicatedNode },
  saveTree: { isPending, message, status }
}) => ({
  defaultLanguage,
  dirty,
  duplicated,
  duplicatedNode,
  isPending,
  message,
  status
});

export default connect(mapStateToProps, { saveTree })(App);
