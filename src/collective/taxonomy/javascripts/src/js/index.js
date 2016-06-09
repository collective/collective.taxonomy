import React from 'react'
import ReactDOM from 'react-dom'
import { Provider } from 'react-redux'

import App from './containers/App'
import DevTools from './containers/DevTools'
import configureStore from './store/configureStore'
import { normalizeData } from './api'

const rootElement = document.getElementById('root')
const taxonomyJson = JSON.parse(rootElement.dataset.taxonomy)

const data = normalizeData(taxonomyJson)

const rootNode = data.entities.nodes[data.result]
const initialState = {
  tree: {
    dirty: false,
    nodes: data.entities.nodes,
  },
  defaultLanguage: rootNode.default_language,
  languages: rootNode.languages,
  rootId: data.result,
}

const store = configureStore(initialState)

if (process.env.NODE_ENV === 'production') {
  /*
   * production mode
   */
  ReactDOM.render(
    <Provider store={ store }>
      <App />
    </Provider>,
    rootElement
    )
} else {
  /*
   * debug/development mode
   */
  ReactDOM.render(
    <div>
      <Provider store={ store }>
        <div>
          <App />
          { process.env.NODE_ENV === 'production' ? null : <DevTools /> }
        </div>
      </Provider>
    </div>,
    rootElement
    )
}
