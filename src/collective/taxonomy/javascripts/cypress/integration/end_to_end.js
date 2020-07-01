/// <reference types="cypress" />

context('Navigation', () => {
  before(() => {
    cy.login();
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
    cy.get('#form-widgets-taxonomies-0').check();
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
    cy.visit('/@@dexterity-types/News%20Item/@@behaviors');
    cy.get('#form-widgets-collective-taxonomy-generated-category-0').check();
    cy.get('#form-buttons-apply').click();
    cy.contains('Behaviors successfully updated.').should('exist');
  })

  it('Add folders', () => {
    cy.addFolder('', 'Portifolio');
    cy.addFolder('/portifolio', 'All museums');
    cy.addFolder('/portifolio', 'Netherlands Museums');
    cy.addFolder('/portifolio', 'France Museums');
  })

  it('Add categorized news items', () => {
    cy.addNewsItem(
      '/portifolio',
      'Centraal Museum',
      'https://www.centraalmuseum.nl/',
      'Centraal_Museum.png',
      'Museums » Netherlands'
    );
    cy.addNewsItem(
      '/portifolio',
      'Zeeuws Museum',
      'https://www.zeeuwsmuseum.nl/',
      'Zeeuws_Museum.png',
      'Museums » Netherlands'
    );
    cy.addNewsItem(
      '/portifolio',
      'Kunsthal KAdE',
      'http://www.kunsthalkade.nl/',
      'Kunsthal_KAdE.png',
      'Museums » Netherlands'
    );
    cy.addNewsItem(
      '/portifolio',
      'Louvre Museum',
      'https://www.louvre.fr',
      'Musee_du_Louvre.png',
      'Museums » France'
    );
  })

  it('Create collections filtering by categories', () => {
    cy.addCollection('/portifolio', 'Portifolio', 4);
    cy.contains('#content', 'Centraal Museum').should('exist');
    cy.contains('#content', 'Zeeuws Museum').should('exist');
    cy.contains('#content', 'Kunsthal KAdE').should('exist');
    cy.contains('#content', 'Louvre Museum').should('exist');

    cy.addCollection('/portifolio/all-museums', 'All Museums', 4);
    cy.contains('#content', 'Centraal Museum').should('exist');
    cy.contains('#content', 'Zeeuws Museum').should('exist');
    cy.contains('#content', 'Kunsthal KAdE').should('exist');
    cy.contains('#content', 'Louvre Museum').should('exist');

    cy.addCollection('/portifolio/netherlands-museums', 'Netherlands Museums', 7);
    cy.contains('#content', 'Centraal Museum').should('exist');
    cy.contains('#content', 'Zeeuws Museum').should('exist');
    cy.contains('#content', 'Kunsthal KAdE').should('exist');
    cy.contains('#content', 'Louvre Museum').should('not.exist');

    cy.addCollection('/portifolio/france-museums', 'France Museums', 6);
    cy.contains('#content', 'Centraal Museum').should('not.exist');
    cy.contains('#content', 'Zeeuws Museum').should('not.exist');
    cy.contains('#content', 'Kunsthal KAdE').should('not.exist');
    cy.contains('#content', 'Louvre Museum').should('exist');
  })
})
