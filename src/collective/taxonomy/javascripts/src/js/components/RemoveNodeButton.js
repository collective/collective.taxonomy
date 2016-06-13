import React, { PropTypes } from 'react'

import Button from './common/Button'

const RemoveNodeButton = ({
  parentId,
  id,
  index,
  removeNode
}) => (
  <Button
    handleClick={ () => removeNode(parentId, id, index) }
    title="Remove this node"
  >
    <i className="icon-minus"></i>
  </Button>
)

RemoveNodeButton.propTypes = {
  parentId: PropTypes.string.isRequired,
  id: PropTypes.string.isRequired,
  index: PropTypes.number.isRequired,
  removeNode: PropTypes.func.isRequired
}

export default RemoveNodeButton
