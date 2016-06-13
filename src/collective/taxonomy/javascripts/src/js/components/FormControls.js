import React, { Component, PropTypes } from 'react'

export default class FormControls extends Component {

  static propTypes = {
    dirty: PropTypes.bool.isRequired,
    saveTree: PropTypes.func.isRequired,
  }

  constructor() {
    super()
    this.handleClick = this.handleClick.bind(this)
  }

  handleClick(e) {
    e.preventDefault()
    this.props.saveTree()
  }

  handleBack(e) {
    e.preventDefault()
    const baseUrl = $('base').attr('href')
    window.location.href = `${baseUrl}/@@taxonomy-settings`
  }

  render() {
    const { dirty } = this.props
    return (
      <div className="formControls">
        <input
          className="context"
          type="submit"
          value="Submit"
          disabled={ !dirty ? 'disabled' : null }
          onClick={ this.handleClick }
        />
        <input
          className="standalone"
          id="back"
          onClick={ this.handleBack }
          type="submit"
          value="Back to settings"
        />
      </div>
    )
  }
}
