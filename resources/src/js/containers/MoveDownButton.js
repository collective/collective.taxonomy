import { connect } from 'react-redux';
import uid from 'uid';

import { moveDown } from '../actions';
import MoveDownButton from '../components/MoveDownButton';

export default connect(null, { moveDown })(MoveDownButton);
