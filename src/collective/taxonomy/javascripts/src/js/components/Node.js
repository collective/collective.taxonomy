import React, { PropTypes } from 'react';
import TreeView from 'react-treeview';

import SubTree from '../containers/SubTree';
import EditableValues from '../containers/EditableValues';
import EditableIds from '../containers/EditableIds';
import AddNodeButton from '../containers/AddNodeButton';
import RemoveNodeButton from '../containers/RemoveNodeButton';
import MoveDownButton from '../containers/MoveDownButton';
import MoveUpButton from '../containers/MoveUpButton';

const Node = ({ duplicatedNode, id, index, language, parentId, subnodes }) => {
  const nodeLabel = (
    <span>
      <sup className="super-text">Title</sup>
      <EditableValues id={id} selectedLanguage={language} />
      &nbsp;&nbsp;&nbsp;
      <sup className="super-text">Id</sup>
      <EditableIds
        id={id}
        index={index}
        parentId={parentId}
        selectedLanguage={language}
        duplicatedNode={duplicatedNode}
      />
      &nbsp;&nbsp;&nbsp;
      <AddNodeButton id={id} index={index} parentId={parentId} />
      <RemoveNodeButton id={id} index={index} parentId={parentId} />
      <MoveDownButton id={id} index={index} parentId={parentId} />
      <MoveUpButton id={id} index={index} parentId={parentId} />
    </span>
  );
  return (
    <TreeView nodeLabel={nodeLabel}>
      {subnodes.map((childId, idx) => (
        <SubTree
          key={childId}
          id={childId}
          index={idx}
          language={language}
          parentId={id}
        />
      ))}
    </TreeView>
  );
};

Node.propTypes = {
  duplicatedNode: PropTypes.string.isRequired,
  id: PropTypes.string.isRequired,
  index: PropTypes.number.isRequired,
  language: PropTypes.string.isRequired,
  parentId: PropTypes.string.isRequired,
  subnodes: PropTypes.array.isRequired,
  title: PropTypes.string.isRequired
};

export default Node;
