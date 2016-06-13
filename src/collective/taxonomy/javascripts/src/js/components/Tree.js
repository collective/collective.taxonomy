import React, { PropTypes } from 'react'
import TreeView from 'react-treeview'

import AddNodeButton from '../containers/AddNodeButton'
import SubTree from '../containers/SubTree'

const Tree = ({
  rootId,
  subnodes,
  title
}) => (
  <TreeView nodeLabel={ title }>
    { subnodes.length === 0 ?
      <AddNodeButton
        index={ 0 }
        parentId={ rootId }
        title="Add a term inside this node"
      >
        <i className="icon-flow-split"></i>
      </AddNodeButton>
      : null }

    { subnodes.map((childId, idx) => (
      <SubTree
        key={ childId }
        id={ childId }
        parentId={ rootId }
        index={ idx }
      />)
    ) }
  </TreeView>
)

Tree.propTypes = {
  rootId: PropTypes.string.isRequired,
  subnodes: PropTypes.array.isRequired,
  title: PropTypes.string.isRequired,
}

export default Tree
