import { connect } from 'react-redux';

import { editTranslation } from '../actions';
import EditableId from '../components/EditableId';

export const mapStateToProps = ({ tree: { nodes } }, { id, language }) => ({
  value: nodes[id].translations[language]
});

export default connect(mapStateToProps, { editTranslation })(EditableId);
