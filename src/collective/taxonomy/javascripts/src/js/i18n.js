import { addLocaleData } from 'react-intl'
import enLocaleData from 'react-intl/locale-data/en'
import frLocaleData from 'react-intl/locale-data/fr'
import translations from './translations'

addLocaleData([...enLocaleData, ...frLocaleData])

export const locale = navigator.language || navigator.browserLanguage
export const translatedMessages = translations[locale]
