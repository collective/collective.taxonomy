#!/bin/sh
# Synchronise the .pot with the templates.
i18ndude rebuild-pot --exclude node_modules --pot locales/collective.taxonomy.pot --create collective.taxonomy .

# Synchronise the resulting .pot with the .po files
i18ndude sync --pot locales/collective.taxonomy.pot locales/*/LC_MESSAGES/collective.taxonomy.po
