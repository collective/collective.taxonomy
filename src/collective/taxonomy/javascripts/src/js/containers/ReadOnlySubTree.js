import { connect } from 'react-redux';

import ReadOnlySubTree from '../components/ReadOnlySubTree';
import { mapStateToProps } from './SubTree';

export default connect(mapStateToProps)(ReadOnlySubTree);
