import React, { Component, PropTypes } from 'react'

import Modal from './Modal'
import InputText from './InputText'
import Button from './common/Button'


export default class EditNodeButton extends Component {

  static propTypes = {
    id: PropTypes.string.isRequired,
    languages: PropTypes.array.isRequired,
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
    const { id, editTranslation, translations, languages } = this.props
    return (
      <span>
        <a onClick={ this.show.bind(this) }>
          <Button title="Edit this node">
            <i className="icon-pencil"></i>
          </Button>
        </a>
        <Modal show={ this.state.show } onClose={ this.close.bind(this) }>
          <div className="pb-ajax">
            <form id="form">
              { languages.map(
                lang => <InputText name={ lang }
                                   key={ lang }
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
