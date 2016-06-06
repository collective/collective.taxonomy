import React, { Component, PropTypes } from 'react'

import Button from './common/Button'


export default class RemoveNodeButton extends Component {

  static propTypes = {
    parentId: PropTypes.string.isRequired,
    id: PropTypes.string.isRequired,
    index: PropTypes.number.isRequired,
    removeNode: PropTypes.func.isRequired
  }

  render() {
    const { parentId, id, index, removeNode, ...other } = this.props
    return (
      <Button handleClick={ () => removeNode(parentId, id, index) }
              { ...other } title="Remove this node"
      >
        <i className="icon-minus"></i>
      </Button>
      )
  }

}
