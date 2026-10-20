const { defineConfig } = require('cypress');

module.exports = defineConfig({
  viewportWidth: 1280,
  e2e: {
    baseUrl: 'http://localhost:8080/Plone',
    // The spec is one sequential scenario: the admin login from before() and
    // the content created by earlier tests must survive across the it() blocks
    // (Cypress 4 behaviour, previously Cypress.Cookies.preserveOnce('__ac')).
    testIsolation: false,
  },
});
