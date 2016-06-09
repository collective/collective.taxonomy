import React, { Component, PropTypes } from 'react'

import EditNodeButton from './EditNodeButton'
import RemoveNodeButton from './RemoveNodeButton'
import AddNodeButton from '../containers/AddNodeButton'


export default class Leaf extends Component {

  static propTypes = {
    defaultLanguage: PropTypes.string.isRequired,
    id: PropTypes.string.isRequired,
    translations: PropTypes.object.isRequired
  }

  render() {
    const { translations, defaultLanguage, ...other } = this.props
    const title = translations[defaultLanguage]
    return (
      <div>
        <div className="info">
          { title || '??????' }&nbsp;&nbsp;&nbsp;
          <EditNodeButton translations={ translations } { ...other } />
          &nbsp;
          <AddNodeButton { ...other } />
          &nbsp;
          <RemoveNodeButton { ...other } />
          &nbsp;
          <AddNodeButton { ...other } parentId={ this.props.id }
                         title="Add a term inside this node"
          >
            <i className="icon-flow-split"></i>
          </AddNodeButton>
        </div>
      </div>
      )
  }

}
