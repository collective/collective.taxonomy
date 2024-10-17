import { connect } from 'react-redux';

import EditableIds from '../components/EditableIds';

export const mapStateToProps = ({ languages }) => ({
  languages: Object.keys(languages)
});

export default connect(mapStateToProps)(EditableIds);
