/// <reference types="cypress" />

const addFolder = (path, title) => {
    cy.visit(`${path}/++add++Folder`);
    cy.get('#form-widgets-IDublinCore-title').type(title);
    cy.saveAndPublish();
};

// term identifiers are generated on save; collected from the category widget
// of the first news item and used for the collection queries below
const termIds = {};

const addNewsItem = (title, site, image, category) => {
  cy.visit('/portfolio/all-museums/++add++News%20Item');
  cy.get('#form-widgets-IDublinCore-title').type(title);
  cy.get('#form-widgets-IDublinCore-description').type(site);
  cy.get('input[type=file]').first().selectFile(`cypress/fixtures/${image}`);
  cy.contains('.autotoc-nav a', 'Categorization').click();
  cy.get('#form-widgets-category-taxonomy_category-from option').each(($option) => {
    termIds[$option.text().trim()] = $option.val();
  });
  cy.get('#form-widgets-category-taxonomy_category-from').select(category);
  cy.get('button[value=→]').click();
  cy.saveAndPublish();
};

// The query goes straight into the pat-querystring field: driving the
// select2 criteria widgets by generated ids was brittle, and the widget
// is Plone's, not ours.
const addCollection = (path, title, term) => {
  cy.visit(`${path}/++add++Collection`);
  cy.get('#form-widgets-IDublinCore-title').type(title);
  cy.get('#form-widgets-ICollection-query').then(($query) => {
    $query.val(
      JSON.stringify([
        {
          i: 'taxonomy_category',
          o: 'plone.app.querystring.operation.selection.any',
          v: [termIds[term]],
        },
      ])
    );
  });
  cy.contains('.autotoc-nav a', 'Settings').click();
  cy.get('#form-widgets-IShortName-id').type('index.html');
  cy.saveAndPublish();
};

context('Navigation', () => {
  before(() => {
    cy.login();
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
    // by value, not by index: a fixture with pre-installed taxonomies
    // (collective.taxonomy:examples) sorts them before the one created above
    cy.get('input[name="form.widgets.taxonomies:list"][value="collective.taxonomy.category"]').check();
    cy.get('#form-buttons-edit_data_taxonomy').click();
    cy.get('.tree-view_children > button').click();

    cy.get('.input-field > input').first().type('Museums');
    cy.get('button[title="Add a term inside this node"]:last').click();
    cy.get('.input-field > input:not(.identifier-input):last').type('Netherlands');
    cy.get('button[title="Add a node at the same level"]:last').click();
    cy.get('.input-field > input:not(.identifier-input):last').type('France');
    cy.get('button[title="Add a node at the same level"]:last').click();
    cy.get('.input-field > input:not(.identifier-input):last').type('England');

    cy.get('button[title="Add a node at the same level"]:first').click();
    cy.get('.input-field > input:not(.identifier-input):last').type('Companies');
    cy.get('button[title="Add a term inside this node"]:last').click();
    cy.get('.input-field > input:not(.identifier-input):last').type('Coca cola');
    cy.get('button[title="Add a node at the same level"]:last').click();
    cy.get('.input-field > input:not(.identifier-input):last').type('Pepsi');
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
    addCollection('/portfolio', 'Portfolio', 'Museums');
    cy.contains('#content', 'Centraal Museum').should('exist');
    cy.contains('#content', 'Zeeuws Museum').should('exist');
    cy.contains('#content', 'Kunsthal KAdE').should('exist');
    cy.contains('#content', 'Louvre Museum').should('exist');

    addCollection('/portfolio/all-museums', 'All Museums', 'Museums');
    cy.contains('#content', 'Centraal Museum').should('exist');
    cy.contains('#content', 'Zeeuws Museum').should('exist');
    cy.contains('#content', 'Kunsthal KAdE').should('exist');
    cy.contains('#content', 'Louvre Museum').should('exist');

    addCollection('/portfolio/netherlands-museums', 'Netherlands Museums', 'Museums » Netherlands');
    cy.contains('#content', 'Centraal Museum').should('exist');
    cy.contains('#content', 'Zeeuws Museum').should('exist');
    cy.contains('#content', 'Kunsthal KAdE').should('exist');
    cy.contains('#content', 'Louvre Museum').should('not.exist');

    addCollection('/portfolio/france-museums', 'France Museums', 'Museums » France');
    cy.contains('#content', 'Centraal Museum').should('not.exist');
    cy.contains('#content', 'Zeeuws Museum').should('not.exist');
    cy.contains('#content', 'Kunsthal KAdE').should('not.exist');
    cy.contains('#content', 'Louvre Museum').should('exist');
  })
})
