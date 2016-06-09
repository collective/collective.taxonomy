import React, { Component, PropTypes } from 'react'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'

import Tree from '../components/Tree'
import MessageBox from '../components/common/MessageBox'
import Spinner from '../components/common/Spinner'
import * as actionCreators from '../actions'


class App extends Component {

  static propTypes = {
    defaultLanguage: PropTypes.string.isRequired,
    dispatch: PropTypes.func.isRequired,
    dirty: PropTypes.bool.isRequired,
    languages: PropTypes.array.isRequired,
    nodes: PropTypes.object.isRequired,
    rootId: PropTypes.string.isRequired,
    saveTree: PropTypes.object.isRequired,
  }

  render() {
    const { defaultLanguage, dispatch, dirty, languages, nodes, rootId,
            saveTree } = this.props
    const boundActionCreators = bindActionCreators(actionCreators, dispatch)
    console.log(boundActionCreators);
    const portalURL = $('base').attr('href')
    const { isPending, message, status } = saveTree
    return (
      <div>

      { isPending ? <Spinner imageURL={ portalURL + '/spinner.gif' } /> : null }

      { status ? <MessageBox status={ status } message={ message } /> : null }

      { dirty ? <MessageBox status="error" message="Changes have been made but you have to click on submit button to save these changes." /> : null }

      <Tree dirty={ dirty } nodes={ nodes } rootId={ rootId }
            defaultLanguage={ defaultLanguage } languages={ languages }
      />
      </div>
      )
  }

}

function select(state) {
  return {
    defaultLanguage: state.defaultLanguage,
    dirty: state.tree.dirty,
    languages: state.languages,
    nodes: state.tree.nodes,
    rootId: state.rootId,
    saveTree: state.saveTree
  }
}

// Wrap the component to inject dispatch and state into it
export default connect(select)(App)
