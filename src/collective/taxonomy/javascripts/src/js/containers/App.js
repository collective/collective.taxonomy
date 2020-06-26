import { connect } from 'react-redux';

import { saveTree } from '../actions';
import App from '../components/App';

const mapStateToProps = ({
  defaultLanguage,
  tree: { dirty },
  saveTree: { isPending, message, status }
}) => ({
  defaultLanguage,
  dirty,
  isPending,
  message,
  status
});

export default connect(mapStateToProps, { saveTree })(App);
