import React, { Component, PropTypes } from 'react'


export default class InputText extends Component {

  static propTypes = {
    action: PropTypes.func.isRequired,
    name: PropTypes.string.isRequired,
    defaultValue: PropTypes.string,
  }

  handleChange(e) {
    e.preventDefault()
    this.props.action(e.target.name, e.target.value)
  }

  render() {
    const { defaultValue, name } = this.props
    const defaultValue_ = defaultValue === undefined ? '' : defaultValue
    return (
      <div className="field">
        <label className="horizontal">{ name }</label>
        <input name={ name } type="text" defaultValue={ defaultValue_ }
               onChange={ this.handleChange.bind(this) }
        />
      </div>
      )
  }

}
