import React, { Component, PropTypes } from 'react'
import uid from 'uid'


export default class AddNodeButton extends Component {

  static propTypes = {
    children: PropTypes.array.isRequired,
    parentId: PropTypes.string.isRequired,
    index: PropTypes.number.isRequired,
    addNode: PropTypes.func.isRequired
  }

  render() {
    // TODO: manage icon
    const { children, index, parentId, addNode } = this.props
    const newKey = uid(10)
    return (
      <button onClick={ () => addNode(parentId, index, newKey) }>
        { children }
      </button>
      )
  }

}
