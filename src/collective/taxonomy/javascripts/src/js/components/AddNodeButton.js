import React, { Component, PropTypes } from 'react'
import uid from 'uid'


export default class AddNodeButton extends Component {

  static propTypes = {
    parentId: PropTypes.string.isRequired,
    index: PropTypes.number.isRequired,
    addNode: PropTypes.func.isRequired
  }

  render() {
    // TODO: manage icon
    const { parentId, index, addNode } = this.props
    const newKey = uid(10)
    return (
      <button onClick={ () => addNode(parentId, index, newKey) }>+</button>
      )
  }

}
