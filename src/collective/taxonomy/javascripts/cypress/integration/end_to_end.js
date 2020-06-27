/// <reference types="cypress" />

context('Navigation', () => {
  before(() => {
    cy.visit('/');
    cy.get('#personaltools-login').click();
    cy.get('#__ac_name').type('admin');
    cy.get('#__ac_password').type('admin');
    cy.get('.pattern-modal-buttons > #buttons-login').click();
    cy.contains('admin').should('exist');
  })

  beforeEach(() => {
    Cypress.Cookies.preserveOnce('__ac');
  })

  it('Add taxonomy', () => {
    cy.visit('/@@taxonomy-settings');
    cy.get('#form-buttons-add-taxonomy').click();
    cy.get('#form-widgets-taxonomy').type('Category');
    cy.get('#form-widgets-field_description').type('Categorize your content type');
    cy.get('#form-widgets-field_title').type('Category');
    cy.get('#form-buttons-add').click();
    cy.contains('Category').should('exist');
  })

  it('Add taxonomy data', () => {
    cy.visit('/@@taxonomy-settings');
    cy.get('#form-widgets-taxonomies-0').click();
    cy.get('#form-buttons-edit_data_taxonomy').click();
    cy.get('.tree-view_children > button').click();
    cy.get('.input-field > input').type('Museums');
    cy.get('button[title="Add a term inside this node"]:last').click();
    cy.get('.input-field > input:last').type('Netherlands');
    cy.get('button[title="Add a node at the same level"]:last').click();
    cy.get('.input-field > input:last').type('France');
    cy.get('button[title="Add a node at the same level"]:last').click();
    cy.get('.input-field > input:last').type('England');
    cy.get('button[title="Add a node at the same level"]:first').click();
    cy.get('.input-field > input:last').type('Companies');
    cy.get('button[title="Add a term inside this node"]:last').click();
    cy.get('.input-field > input:last').type('Coca cola');
    cy.get('button[title="Add a node at the same level"]:last').click();
    cy.get('.input-field > input:last').type('Pepsi');
    cy.get('#form-buttons-save').click();
    cy.contains('Your taxonomy has been saved with success').should('exist');
  })

  it('Enable behavior', () => {
    cy.visit('/@@dexterity-types/Document/@@behaviors');
    cy.get('#form-widgets-collective-taxonomy-generated-category-0').click();
    cy.get('#form-buttons-apply').click();
    cy.contains('Behaviors successfully updated.').should('exist');
  })

  it('Add categorized pages', () => {
    cy.visit('/++add++Document');
    cy.get('#form-widgets-IDublinCore-title').type('Centraal Museum');
    cy.get('#form-widgets-IDublinCore-description').type('https://www.centraalmuseum.nl/');
    cy.get('#autotoc-item-autotoc-2').click();
    cy.get('#form-widgets-category-taxonomy_category-from').select('Museums » Netherlands');
    cy.get('button[value=↓]').click();
    cy.get('#form-buttons-save').click();
    cy.contains('Item created').should('exist');

    cy.visit('/++add++Document');
    cy.get('#form-widgets-IDublinCore-title').type('Zeeuws Museum');
    cy.get('#form-widgets-IDublinCore-description').type('https://www.zeeuwsmuseum.nl/');
    cy.get('#autotoc-item-autotoc-2').click();
    cy.get('#form-widgets-category-taxonomy_category-from').select('Museums » Netherlands');
    cy.get('button[value=↓]').click();
    cy.get('#form-buttons-save').click();
    cy.contains('Item created').should('exist');

    cy.visit('/++add++Document');
    cy.get('#form-widgets-IDublinCore-title').type('Kunsthal KAdE');
    cy.get('#form-widgets-IDublinCore-description').type('http://www.kunsthalkade.nl/');
    cy.get('#autotoc-item-autotoc-2').click();
    cy.get('#form-widgets-category-taxonomy_category-from').select('Museums » Netherlands');
    cy.get('button[value=↓]').click();
    cy.get('#form-buttons-save').click();
    cy.contains('Item created').should('exist');

    cy.visit('/++add++Document');
    cy.get('#form-widgets-IDublinCore-title').type('Louvre Museum');
    cy.get('#form-widgets-IDublinCore-description').type('https://www.louvre.fr');
    cy.get('#autotoc-item-autotoc-2').click();
    cy.get('#form-widgets-category-taxonomy_category-from').select('Museums » France');
    cy.get('button[value=↓]').click();
    cy.get('#form-buttons-save').click();
    cy.contains('Item created').should('exist');
  })

  it('Create collections filtering by categories', () => {
    cy.visit('/++add++Collection');
    cy.get('#form-widgets-IDublinCore-title').type('Netherlands Museums');
    cy.get('#select2-chosen-12').click();
    cy.get('.select2-result-label:last').click();
    cy.get('ul.select2-choices:first').click();
    cy.get('#select2-drop > ul > li:nth-child(7) > div').click();
    cy.wait(1000);
    cy.get('#form-buttons-save').click();
    cy.contains('#content', 'Centraal Museum').should('exist');
    cy.contains('#content', 'Zeeuws Museum').should('exist');
    cy.contains('#content', 'Kunsthal KAdE').should('exist');
    cy.contains('#content', 'Louvre Museum').should('not.exist');

    cy.visit('/++add++Collection');
    cy.get('#form-widgets-IDublinCore-title').type('France Museums');
    cy.get('#select2-chosen-12').click();
    cy.get('.select2-result-label:last').click();
    cy.get('ul.select2-choices:first').click();
    cy.get('#select2-drop > ul > li:nth-child(6) > div').click();
    cy.wait(1000);
    cy.get('#form-buttons-save').click();
    cy.contains('#content', 'Centraal Museum').should('not.exist');
    cy.contains('#content', 'Zeeuws Museum').should('not.exist');
    cy.contains('#content', 'Kunsthal KAdE').should('not.exist');
    cy.contains('#content', 'Louvre Museum').should('exist');

    cy.visit('/++add++Collection');
    cy.get('#form-widgets-IDublinCore-title').type('All Museums');
    cy.get('#select2-chosen-12').click();
    cy.get('.select2-result-label:last').click();
    cy.get('ul.select2-choices:first').click();
    cy.get('#select2-drop > ul > li:nth-child(4) > div').click();
    cy.wait(1000);
    cy.get('#form-buttons-save').click();
    cy.contains('#content', 'Centraal Museum').should('exist');
    cy.contains('#content', 'Zeeuws Museum').should('exist');
    cy.contains('#content', 'Kunsthal KAdE').should('exist');
    cy.contains('#content', 'Louvre Museum').should('exist');
  })
})
