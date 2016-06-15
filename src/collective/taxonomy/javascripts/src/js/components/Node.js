import React, { PropTypes } from 'react'
import TreeView from 'react-treeview'

import SubTree from '../containers/SubTree'
import EditableValues from '../containers/EditableValues'
import AddNodeButton from '../containers/AddNodeButton'
import RemoveNodeButton from '../containers/RemoveNodeButton'

const Node = ({ id, index, language, parentId, subnodes }) => {
  const nodeLabel = (
    <span>
      <EditableValues id={ id } selectedLanguage={ language } />
      &nbsp;&nbsp;&nbsp;
      <AddNodeButton
        id={ id }
        index={ index }
        parentId={ parentId }
      />
      <RemoveNodeButton
        id={ id }
        index={ index }
        parentId={ parentId }
      />
    </span>
  )
  return (
    <TreeView nodeLabel={ nodeLabel }>
      { subnodes.map((childId, idx) => (
        <SubTree
          key={ childId }
          id={ childId }
          index={ idx }
          language={ language }
          parentId={ id }
        />))
      }
    </TreeView>
  )
}

Node.propTypes = {
  id: PropTypes.string.isRequired,
  index: PropTypes.number.isRequired,
  language: PropTypes.string.isRequired,
  parentId: PropTypes.string.isRequired,
  subnodes: PropTypes.array.isRequired,
  title: PropTypes.string.isRequired,
}

export default Node
