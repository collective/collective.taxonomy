import React, { Component, PropTypes } from 'react'

import Leaf from './Leaf'
import Node from './Node'


export default class SubTree extends Component {

  static propTypes = {
    subnodes: PropTypes.array.isRequired
  }

  render() {
    const { subnodes, ...other } = this.props
    return (
      subnodes.length > 0 ? (
          <Node { ...other } subnodes={ subnodes } />
        ) : (
          <Leaf { ...other } />
        )
      )
  }

}
