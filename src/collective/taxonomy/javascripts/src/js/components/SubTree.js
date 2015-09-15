import React, { Component, PropTypes } from 'react'

import Leaf from './Leaf'
import Node from './Node'


export default class SubTree extends Component {

  static propTypes = {
    children: PropTypes.array.isRequired
  }

  render() {
    const { children, ...other } = this.props
    return (
      children.length > 0 ? (
          <Node { ...other } children={ children } />
        ) : (
          <Leaf { ...other } />
        )
      )
  }

}
