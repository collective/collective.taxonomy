import React, { Component, PropTypes } from 'react'
import TreeView from 'react-treeview'

import SubTree from './SubTree'
import EditNodeButton from './EditNodeButton'
import AddNodeButton from '../containers/AddNodeButton'
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
    const subnodes = nodes[id].subnodes
    const title = translations[defaultLanguage]
    const nodeLabel = (
      <span>
        { title || '??????' }&nbsp;&nbsp;&nbsp;
        <EditNodeButton { ...other } id={ id } translations={ translations } />
        <AddNodeButton { ...other } />
        <RemoveNodeButton { ...other } id={ id } />
      </span>
      )
    return (
      <TreeView nodeLabel={ nodeLabel }>
        { subnodes.map((childId, index) => (
          <SubTree { ...other }
                   key={ childId }
                   id={ childId }
                   index={ index }
                   parentId={ id }
                   nodes={ nodes }
                   defaultLanguage={ defaultLanguage }
                   translations={ translations }
                   { ...nodes[childId] }
          />))
        }
      </TreeView>
      )
  }

}
