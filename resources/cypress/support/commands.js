// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add("login", (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add("drag", { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add("dismiss", { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite("visit", (originalFn, url, options) => { ... })

// Credentials default to the buildout instance (admin/admin); against the
// plone.app.testing fixture of `bin/robot-server collective.taxonomy.testing.ROBOT_TESTING`
// run with CYPRESS_USER=admin CYPRESS_PASSWORD=secret CYPRESS_BASE_URL=http://localhost:55001/plone
Cypress.Commands.add('login', () => {
  cy.visit('/');
  if (/__ac/.test(document.cookie)) {
    return;
  }
  cy.get('#personaltools-login').click();
  cy.env(['USER', 'PASSWORD']).then(({ USER, PASSWORD }) => {
    cy.get('#__ac_name').type(USER || 'admin');
    cy.get('#__ac_password').type(PASSWORD || 'admin', { log: false });
  });
  cy.get('.pattern-modal-buttons > #buttons-login').click();
  cy.contains('admin').should('exist');
});

Cypress.Commands.add('saveAndPublish', () => {
  cy.get('#form-buttons-save').click();
  cy.contains('Item created').should('exist');
  cy.get('.label-state-private').click();
  cy.get('#workflow-transition-publish').click();
  cy.contains('Item state changed.').should('exist');
});
