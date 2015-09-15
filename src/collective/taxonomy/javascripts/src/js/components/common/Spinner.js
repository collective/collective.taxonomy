import React, { Component, PropTypes } from 'react'


export default class Spinner extends Component {

  static propTypes = {
    imageURL: PropTypes.string.isRequired,
  }

  render() {
    const imageURL = this.props.imageURL
    return (
        <div id="ajax-spinner" style={ { display: 'block' } }>
          <img src={ imageURL } alt=""/>
        </div>
      )
  }

}
