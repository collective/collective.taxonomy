import { connect } from 'react-redux';

import { editIdentifier } from '../actions';
import EditableId from '../components/EditableId';

export const mapStateToProps = ({ tree: { nodes } }, { id, language }) => ({
  value: nodes[id].translations[language]
});

export default connect(mapStateToProps, { editIdentifier })(EditableId);
