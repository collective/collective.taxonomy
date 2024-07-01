import { addLocaleData } from 'react-intl';
import enLocaleData from 'react-intl/locale-data/en';
import esLocaleData from 'react-intl/locale-data/es';
import frLocaleData from 'react-intl/locale-data/fr';
import nlLocaleData from 'react-intl/locale-data/nl';
import translations from './translations';

addLocaleData([...enLocaleData, ...esLocaleData]);
addLocaleData([...enLocaleData, ...frLocaleData]);
addLocaleData([...enLocaleData, ...nlLocaleData]);

// use Plone portal language
export const locale = document.querySelector('html').getAttribute('lang');
export const translatedMessages = translations[locale];
