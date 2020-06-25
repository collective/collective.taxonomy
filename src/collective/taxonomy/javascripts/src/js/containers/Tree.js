import { connect } from 'react-redux';

import Tree from '../components/Tree';

export const mapStateToProps = ({
  languages,
  rootId,
  selectedLanguage,
  tree: { nodes }
}) => ({
  nodes,
  subnodes: nodes[rootId].subnodes,
  rootId,
  selectedLanguage: languages[selectedLanguage].toLowerCase(),
  title: nodes[rootId].title
});

export default connect(mapStateToProps)(Tree);
