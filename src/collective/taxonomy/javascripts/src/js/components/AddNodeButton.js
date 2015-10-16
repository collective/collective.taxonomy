import React, { Component, PropTypes } from 'react'
import uid from 'uid'

import Button from './common/Button'


export default class AddNodeButton extends Component {

  static propTypes = {
    parentId: PropTypes.string.isRequired,
    children: React.PropTypes.oneOfType([
      React.PropTypes.array,
      React.PropTypes.element,
      React.PropTypes.string]),
    index: PropTypes.number.isRequired,
    index: PropTypes.string,
    addNode: PropTypes.func.isRequired
  }

  render() {
    // TODO: manage icon
    const { addNode, children, index, parentId, title, ...other } = this.props
    const newKey = uid(10)
    return (
      <Button handleClick={ () => addNode(parentId, index, newKey) }
              { ...other }
              title={ title ? title : 'Add a node at the same level' }
      >
        { children ? children : <i className="icon-plus"></i> }
      </Button>
      )
  }

}
