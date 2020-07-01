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

Cypress.Commands.add('login', () => {
  cy.visit('/');
  if (/__ac/.test(document.cookie)) {
    return;
  }
  cy.get('#personaltools-login').click();
  cy.get('#__ac_name').type('admin');
  cy.get('#__ac_password').type('admin');
  cy.get('.pattern-modal-buttons > #buttons-login').click();
  cy.contains('admin').should('exist');
});

Cypress.Commands.add('uploadFile', { prevSubject: true }, (subject, fileName, fileType = '') => {
  cy.fixture(fileName,'binary').then(content => {
    return Cypress.Blob.binaryStringToBlob(content, fileType).then(blob => {
      const el = subject[0];
      const testFile = new File([blob], fileName, {type: fileType});
      const dataTransfer = new DataTransfer();

      dataTransfer.items.add(testFile);
      el.files = dataTransfer.files;
      cy.wrap(subject).trigger('change', { force: true });
    });
  });
});

Cypress.Commands.add('saveAndPublish', () => {
  cy.get('#form-buttons-save').click();
  cy.contains('Item created').should('exist');
  cy.get('.label-state-private').click();
  cy.get('#workflow-transition-publish').click();
  cy.contains('Item state changed.').should('exist');
});

Cypress.Commands.add('addFolder', (path, title) => {
    cy.visit(`${path}/++add++Folder`);
    cy.get('#form-widgets-IDublinCore-title').type(title);
    cy.saveAndPublish();
});

Cypress.Commands.add('addNewsItem', (path, title, site, image, category) => {
  cy.visit(`${path}/++add++News%20Item`);
  cy.get('#form-widgets-IDublinCore-title').type(title);
  cy.get('#form-widgets-IDublinCore-description').type(site);
  cy.get('input[type=file]').uploadFile(image, 'image/png');
  cy.get('#autotoc-item-autotoc-1').click();
  cy.get('#form-widgets-category-taxonomy_category-from').select(category);
  cy.get('button[value=↓]').click();
  cy.saveAndPublish();
});

Cypress.Commands.add('addCollection', (path, title, index) => {
  cy.visit(`${path}/++add++Collection`);
  cy.get('#form-widgets-IDublinCore-title').type(title);
  cy.get('#select2-chosen-12').click();
  cy.get('.select2-result-label:last').click();
  cy.get('ul.select2-choices:first').click();
  cy.get(`#select2-drop > ul > li:nth-child(${index}) > div`).click();
  cy.wait(1000);
  cy.get('#autotoc-item-autotoc-1').click();
  cy.get('#form-widgets-IShortName-id').type('index.html');
  cy.saveAndPublish();
});
