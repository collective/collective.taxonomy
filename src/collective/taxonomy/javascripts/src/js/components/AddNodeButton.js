import React, { PropTypes } from 'react'

import Button from './common/Button'

const AddNodeButton = ({
  addNode,
  children,
  title
}) => (
  <Button
    handleClick={ addNode }
    title={ title || 'Add a node at the same level' }
  >
    { children || <i className="icon-plus"></i> }
  </Button>
)

AddNodeButton.propTypes = {
  // parentId: PropTypes.string.isRequired,
  children: React.PropTypes.oneOfType([
    React.PropTypes.array,
    React.PropTypes.element,
    React.PropTypes.string]),
  // index: PropTypes.number.isRequired,
  title: PropTypes.string,
  addNode: PropTypes.func.isRequired,
}

export default AddNodeButton
