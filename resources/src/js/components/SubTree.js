import React, { PropTypes } from 'react';

import Leaf from './Leaf';
import Node from './Node';

const SubTree = ({
  duplicatedNode,
  id,
  index,
  language,
  subnodes,
  title,
  parentId
}) =>
  subnodes.length > 0 ? (
    <Node
      id={id}
      index={index}
      language={language}
      parentId={parentId}
      subnodes={subnodes}
      title={title}
      duplicatedNode={duplicatedNode}
    />
  ) : (
    <Leaf
      id={id}
      index={index}
      language={language}
      parentId={parentId}
      title={title}
      duplicatedNode={duplicatedNode}
    />
  );

SubTree.propTypes = {
  duplicatedNode: PropTypes.string.isRequired,
  id: PropTypes.string.isRequired,
  index: PropTypes.number.isRequired,
  language: PropTypes.string.isRequired,
  parentId: PropTypes.string.isRequired,
  subnodes: PropTypes.array.isRequired,
  title: PropTypes.string
};

SubTree.defaultProps = {
  title: ''
};

export default SubTree;
