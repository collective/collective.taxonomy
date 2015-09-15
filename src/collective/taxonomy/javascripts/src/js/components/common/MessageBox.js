import React, { Component, PropTypes } from 'react'


export default class MessageBox extends Component {

  static propTypes = {
    message: PropTypes.string.isRequired,
    status: PropTypes.string.isRequired,
  }

  render() {
    const { message, status } = this.props
    return (
      <dl className={ 'portalMessage ' + status }>
        <dt>{ status }</dt>
        <dd>{ message }</dd>
      </dl>
      )
  }

}
