import { connect } from 'react-redux';
import uid from 'uid';

import { moveUp } from '../actions';
import MoveUpButton from '../components/MoveUpButton';

export default connect(null, { moveUp })(MoveUpButton);
