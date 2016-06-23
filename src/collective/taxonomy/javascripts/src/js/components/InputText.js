import React, { Component, PropTypes } from 'react'

export default class InputText extends Component {

  static propTypes = {
    action: PropTypes.func.isRequired,
    name: PropTypes.string.isRequired,
    defaultValue: PropTypes.string,
  }

  static defaultProps = {
    defaultValue: ''
  }

  constructor() {
    super()
    this.handleChange = this.handleChange.bind(this)
  }

  handleChange(e) {
    e.preventDefault()
    this.props.action(e.target.name, e.target.value)
  }

  render() {
    const { defaultValue, name } = this.props
    return (
      <div className="field">
        <label className="horizontal">{ name }</label>
        <input
          defaultValue={ defaultValue }
          name={ name }
          onChange={ this.handleChange }
          type="text"
        />
      </div>
      )
  }

}
