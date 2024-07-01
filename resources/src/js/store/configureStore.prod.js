import { createStore, applyMiddleware } from 'redux';

import middlewares from './middlewares';
import rootReducer from '../reducers';

export default function configureStore(initialState) {
  return createStore(
    rootReducer,
    initialState,
    applyMiddleware(...middlewares)
  );
}
