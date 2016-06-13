import React, { PropTypes } from 'react'

import AddNodeButton from '../containers/AddNodeButton'
import EditableValues from '../containers/EditableValues'
import RemoveNodeButton from '../containers/RemoveNodeButton'

const Leaf = ({ id, index, parentId, title }) => (
  <div>
    <div className="info">
      <EditableValues id={ id } />
      &nbsp;&nbsp;&nbsp;
      <AddNodeButton
        index={ index }
        parentId={ parentId }
      />
      &nbsp;
      <RemoveNodeButton
        id={ id }
        index={ index }
        parentId={ parentId }
        title={ title }
      />
      &nbsp;
      <AddNodeButton
        index={ index }
        parentId={ id }
        title="Add a term inside this node"
      >
        <i className="icon-flow-split"></i>
      </AddNodeButton>
    </div>
  </div>
)

Leaf.propTypes = {
  id: PropTypes.string.isRequired,
  index: PropTypes.number.isRequired,
  parentId: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
}

export default Leaf
