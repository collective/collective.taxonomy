import React, { PropTypes } from 'react';
import TreeView from 'react-treeview';

import EditableTree from './EditableTree';
import ReadOnlySubTree from '../containers/ReadOnlySubTree';

const Tree = ({ editable, duplicatedNode, ...rest }) => {
  if (editable) {
    return <EditableTree duplicatedNode={duplicatedNode} {...rest} />;
  }

  return (
    <TreeView nodeLabel={rest.title}>
      {rest.subnodes.map(childId => (
        <ReadOnlySubTree key={childId} id={childId} {...rest} />
      ))}
    </TreeView>
  );
};

Tree.propTypes = {
  editable: PropTypes.bool.isRequired
};

export default Tree;
