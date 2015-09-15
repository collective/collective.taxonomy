import React, { Component, PropTypes } from 'react'

import Modal from './Modal'
import InputText from './InputText'


export default class EditNodeButton extends Component {

  static propTypes = {
    id: PropTypes.string.isRequired,
    translations: PropTypes.object.isRequired,
    editTranslation: PropTypes.func.isRequired
  }

  constructor() {
    super()
    this.state = {}
  }

  show() {
    this.setState({ show: true })
  }

  close() {
    this.setState({ show: false })
  }

  render() {
    const { id, editTranslation, translations } = this.props
    return (
      <span>
        <a onClick={ this.show.bind(this) }><button>Edit</button></a>
        <Modal show={ this.state.show } onClose={ this.close.bind(this) }>
          <div className="pb-ajax">
            <form id="form">
              { Object.keys(translations).map(
                lang => <InputText name={ lang }
                                   defaultValue={ translations[lang] }
                                   action={ (language, value) => editTranslation(id, language, value) }
                        />
                ) }
            </form>
          </div>
        </Modal>
      </span>
      )
  }

}
