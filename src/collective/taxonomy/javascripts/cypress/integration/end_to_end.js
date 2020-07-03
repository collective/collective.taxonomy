/// <reference types="cypress" />

const addFolder = (path, title) => {
    cy.visit(`${path}/++add++Folder`);
    cy.get('#form-widgets-IDublinCore-title').type(title);
    cy.saveAndPublish();
};

const addNewsItem = (title, site, image, category) => {
  cy.visit('/portfolio/all-museums/++add++News%20Item');
  cy.get('#form-widgets-IDublinCore-title').type(title);
  cy.get('#form-widgets-IDublinCore-description').type(site);
  cy.get('input[type=file]').uploadFile(image, 'image/png');
  cy.get('#autotoc-item-autotoc-1').click();
  cy.get('#form-widgets-category-taxonomy_category-from').select(category);
  cy.get('button[value=↓]').click();
  cy.saveAndPublish();
};

const addCollection = (path, title, index) => {
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
};

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
    addFolder('', 'Portfolio');
    addFolder('/portfolio', 'All museums');
    addFolder('/portfolio', 'Netherlands Museums');
    addFolder('/portfolio', 'France Museums');
  })

  it('Add categorized news items', () => {
    addNewsItem(
      'Centraal Museum',
      'https://www.centraalmuseum.nl/',
      'Centraal_Museum.png',
      'Museums » Netherlands'
    );
    addNewsItem(
      'Zeeuws Museum',
      'https://www.zeeuwsmuseum.nl/',
      'Zeeuws_Museum.png',
      'Museums » Netherlands'
    );
    addNewsItem(
      'Kunsthal KAdE',
      'http://www.kunsthalkade.nl/',
      'Kunsthal_KAdE.png',
      'Museums » Netherlands'
    );
    addNewsItem(
      'Louvre Museum',
      'https://www.louvre.fr',
      'Musee_du_Louvre.png',
      'Museums » France'
    );
  })

  it('Create collections filtering by categories', () => {
    addCollection('/portfolio', 'Portfolio', 4);
    cy.contains('#content', 'Centraal Museum').should('exist');
    cy.contains('#content', 'Zeeuws Museum').should('exist');
    cy.contains('#content', 'Kunsthal KAdE').should('exist');
    cy.contains('#content', 'Louvre Museum').should('exist');

    addCollection('/portfolio/all-museums', 'All Museums', 4);
    cy.contains('#content', 'Centraal Museum').should('exist');
    cy.contains('#content', 'Zeeuws Museum').should('exist');
    cy.contains('#content', 'Kunsthal KAdE').should('exist');
    cy.contains('#content', 'Louvre Museum').should('exist');

    addCollection('/portfolio/netherlands-museums', 'Netherlands Museums', 7);
    cy.contains('#content', 'Centraal Museum').should('exist');
    cy.contains('#content', 'Zeeuws Museum').should('exist');
    cy.contains('#content', 'Kunsthal KAdE').should('exist');
    cy.contains('#content', 'Louvre Museum').should('not.exist');

    addCollection('/portfolio/france-museums', 'France Museums', 6);
    cy.contains('#content', 'Centraal Museum').should('not.exist');
    cy.contains('#content', 'Zeeuws Museum').should('not.exist');
    cy.contains('#content', 'Kunsthal KAdE').should('not.exist');
    cy.contains('#content', 'Louvre Museum').should('exist');
  })
})
