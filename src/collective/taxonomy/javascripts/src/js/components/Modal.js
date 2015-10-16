import React, { Component, PropTypes } from 'react'


export default class Modal extends Component {

  static propTypes = {
    show: PropTypes.bool,
    children: PropTypes.object.isRequired,
    onClose: PropTypes.func.isRequired,
  }

  setPloneOverlayStyle(component) {
    const overlay = React.findDOMNode(component)
    if (!overlay) return
    const height = overlay.outerHeight
    const width = document.body.clientWidth * 0.6
    overlay.style.left = (document.body.clientWidth / 2 - width / 2)
    overlay.style.top = (document.body.outerHeight / 2 - height / 2)
    overlay.style.width = width + 'px'
    overlay.style.zIndex = '9999'
    overlay.style.position = 'absolute'
    overlay.style.display = 'block'
  }

  handleClose(e) {
    e.preventDefault()
    this.props.onClose()
  }

  render() {
    const { show, children } = this.props
    if (!show) return null
    return (
      <div className="overlay overlay-ajax" ref={ this.setPloneOverlayStyle }>
        <div className="close" onClick={ this.handleClose.bind(this) }>
          <a href="#" className="hiddenStructure" title="Close this box">
            Close this box.
          </a>
        </div>
        <div className="pb-ajax">
          <div>
            { children }
          </div>
        </div>
      </div>
      )
  }
}
