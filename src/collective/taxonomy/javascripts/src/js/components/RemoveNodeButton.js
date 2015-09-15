import React, { Component, PropTypes } from 'react'


export default class RemoveNodeButton extends Component {

  static propTypes = {
    parentId: PropTypes.string.isRequired,
    id: PropTypes.string.isRequired,
    index: PropTypes.number.isRequired,
    removeNode: PropTypes.func.isRequired
  }

  render() {
    // TODO: manage icon
    const { parentId, id, index, removeNode } = this.props
    return (
      <button onClick={ () => removeNode(parentId, id, index) }>-</button>
      )
  }

}
