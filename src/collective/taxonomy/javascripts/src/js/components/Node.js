import React, { Component, PropTypes } from 'react'
import TreeView from 'react-treeview'

import SubTree from './SubTree'
import EditNodeButton from './EditNodeButton'
import AddNodeButton from './AddNodeButton'
import RemoveNodeButton from './RemoveNodeButton'


export default class Node extends Component {

  static propTypes = {
    id: PropTypes.string.isRequired,
    nodes: PropTypes.object.isRequired,
    translations: PropTypes.object.isRequired,
    defaultLanguage: PropTypes.string.isRequired,
  }

  render() {
    const { id, nodes, translations, defaultLanguage, ...other } = this.props
    const children = nodes[id].children
    const title = translations[defaultLanguage]
    const nodeLabel = (
      <span>
        { title }&nbsp;&nbsp;&nbsp;
        <EditNodeButton id={ id } translations={ translations } { ...other } />
        <AddNodeButton { ...other } />
        <RemoveNodeButton { ...other } id={ id } />
      </span>
      )
    return (
      <TreeView nodeLabel={ nodeLabel }>
        { children.map((childId, index) => (
          <SubTree { ...other }
                   id={ childId }
                   index={ index }
                   parentId={ id }
                   nodes={ nodes }
                   defaultLanguage={ defaultLanguage }
                   { ...nodes[childId] }
          />))
        }
      </TreeView>
      )
  }

}
