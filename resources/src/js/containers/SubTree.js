import { connect } from 'react-redux';

import SubTree from '../components/SubTree';
import { editTranslation } from '../actions';

export const mapStateToProps = ({ tree: { nodes } }, { id, language }) => {
  const node = nodes[id];
  return {
    subnodes: node.subnodes,
    title: node.translations[language]
  };
};

export default connect(mapStateToProps, { editTranslation })(SubTree);
