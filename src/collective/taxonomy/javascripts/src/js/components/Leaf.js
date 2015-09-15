import React, { Component, PropTypes } from 'react'

import EditNodeButton from './EditNodeButton'
import AddNodeButton from './AddNodeButton'
import RemoveNodeButton from './RemoveNodeButton'


export default class Leaf extends Component {

  static propTypes = {
    defaultLanguage: PropTypes.string.isRequired,
    translations: PropTypes.object.isRequired
  }

  render() {
    const { translations, defaultLanguage, ...other } = this.props
    const title = translations[defaultLanguage]
    return (
      <div>
        <div className="info">
          { title }&nbsp;&nbsp;&nbsp;
          <EditNodeButton translations={ translations } { ...other } />
          <AddNodeButton { ...other } />
          <RemoveNodeButton { ...other } />
        </div>
      </div>
      )
  }

}
