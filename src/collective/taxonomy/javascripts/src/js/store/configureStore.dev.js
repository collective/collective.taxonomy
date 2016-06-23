import { createStore, compose, applyMiddleware } from 'redux'
import { persistState } from 'redux-devtools'
import middlewares from './middlewares'

import rootReducer from '../reducers'
import DevTools from '../containers/DevTools'

export default function configureStore(initialState) {
  const store = createStore(
    rootReducer,
    initialState,
    compose(
      applyMiddleware(...middlewares),
      DevTools.instrument(),
      persistState(
        window.location.href.match(
          /[?&]debug_session=([^&]+)\b/
        )
      )
    )
  )
  if (module.hot) {
    module.hot.accept('../reducers', () => store.replaceReducer(rootReducer))
  }
  return store
}
