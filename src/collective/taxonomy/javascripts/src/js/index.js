import React from 'react'
import ReactDOM from 'react-dom'
import { Provider } from 'react-redux'
import { combineReducers, createStore, compose, applyMiddleware } from 'redux'
import { devTools, persistState } from 'redux-devtools'
import promiseMiddleware from 'redux-promise-middleware'

// import createDevToolsWindow from './createDevToolsWindow'
import App from './containers/App'
import * as reducers from './reducers'
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
  rootId: data.result,
}

const reducer = combineReducers(reducers)


if (process.env.NODE_ENV === 'production') {
  /*
   * production mode
   */

  const createStoreWithMiddleware = applyMiddleware(
    promiseMiddleware
  )(createStore)

  const store = createStoreWithMiddleware(reducer, initialState)
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

  const finalCreateStore = compose(
    applyMiddleware(promiseMiddleware),
    devTools(),
    persistState(window.location.href.match(/[?&]debug_session=([^&]+)\b/))
  )(createStore)

  const store = finalCreateStore(reducer, initialState)
  ReactDOM.render(
    <div>
      <Provider store={ store }>
        <App />
      </Provider>
    </div>,
    rootElement
    )

  // createDevToolsWindow(store)
}
