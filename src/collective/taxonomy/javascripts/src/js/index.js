import React from 'react';
import ReactDOM from 'react-dom';
import { IntlProvider } from 'react-intl';
import { Provider } from 'react-redux';

import App from './containers/App';
import DevTools from './containers/DevTools';
import configureStore from './store/configureStore';
import { normalizeData } from './api';
import { locale, translatedMessages } from './i18n';

const rootElement = document.getElementById('root');
const taxonomyJson = JSON.parse(rootElement.dataset.taxonomy);
const languagesMapping = JSON.parse(rootElement.dataset.languages);

const data = normalizeData(taxonomyJson);

const rootNode = data.entities.nodes[data.result];
const initialState = {
  tree: {
    dirty: false,
    nodes: data.entities.nodes
  },
  defaultLanguage: rootNode.default_language,
  languages: languagesMapping,
  rootId: data.result,
  selectedLanguage: rootNode.default_language
};

const store = configureStore(initialState);

if (process.env.NODE_ENV === 'production') {
  /*
   * production mode
   */
  ReactDOM.render(
    <IntlProvider locale={locale} messages={translatedMessages}>
      <Provider store={store}>
        <App />
      </Provider>
    </IntlProvider>,
    rootElement
  );
} else {
  /*
   * debug/development mode
   */
  ReactDOM.render(
    <div>
      <IntlProvider locale={locale} messages={translatedMessages}>
        <Provider store={store}>
          <div>
            <App />
            {process.env.NODE_ENV === 'production' ? null : <DevTools />}
          </div>
        </Provider>
      </IntlProvider>
    </div>,
    rootElement
  );
}
