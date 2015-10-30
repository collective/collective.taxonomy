import React, { Component, PropTypes } from 'react'
import TreeView from 'react-treeview'

import SubTree from './SubTree'


export default class Tree extends Component {

  static propTypes = {
    defaultLanguage: PropTypes.string.isRequired,
    dirty: PropTypes.bool.isRequired,
    nodes: PropTypes.object.isRequired,
    rootId: PropTypes.string.isRequired,
    saveTree: PropTypes.func.isRequired,
  }

  handleClick(e) {
    const { nodes, rootId, saveTree } = this.props
    e.preventDefault()
    saveTree(nodes, rootId)
  }

  handleBack(e) {
    e.preventDefault()
    window.location.href = $('base').attr('href') + '/@@taxonomy-settings'
  }

  render() {
    const { dirty, rootId, nodes, defaultLanguage, ...other } = this.props
    const label = nodes[rootId].title
    const subnodes = nodes[rootId].subnodes
    return (
      <div>
      <h1>Edit taxonomy data</h1>
      <TreeView key={ rootId } nodeLabel={ label }>
        { subnodes.map((childId, index) => (
          <SubTree id={ childId }
                   parentId={ rootId }
                   defaultLanguage={ defaultLanguage }
                   index={ index }
                   nodes={ nodes }
                   { ...other }
                   { ...nodes[childId] }
          />)
        ) }
      </TreeView>
      <div className="formControls">
        <input className="submit-widget button-field context allowMultiSubmit"
               type="submit" value="Submit"
               disabled={ !dirty ? 'disabled' : null }
               onClick={ this.handleClick.bind(this) }
        />


        <input className="submit-widget button-field standalone" id="back"
               onClick={ this.handleBack } type="submit"
               value="Back to settings"
        />
      </div>
      </div>
      )
  }

}
