import React, { Component, PropTypes } from 'react'


export default class InputText extends Component {

  static propTypes = {
    action: PropTypes.func.isRequired,
    name: PropTypes.string.isRequired,
    defaultValue: PropTypes.string.isRequired,
  }

  handleChange(e) {
    e.preventDefault()
    this.props.action(e.target.name, e.target.value)
  }

  render() {
    const { name, defaultValue } = this.props
    return (
      <div className="field">
        <label className="horizontal">{ name }</label>
        <input name={ name } type="text" defaultValue={ defaultValue }
               onChange={ this.handleChange.bind(this) }
        />
      </div>
      )
  }

}
