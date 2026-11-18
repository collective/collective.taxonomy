import type { Page } from '@playwright/test';
import path from 'node:path';

import { login } from './login';
import { expect, test } from './test';

const FIXTURES = path.join(__dirname, '..', 'fixtures');

const CATEGORY_FROM = '#form-widgets-category-taxonomy_category-from';

// Term identifiers are generated on save; they are collected from the
// category widget of the first news item and used for the collection queries.
type TermIds = Record<string, string>;

async function saveAndPublish(page: Page) {
  await page.locator('#form-buttons-save').click();
  await expect(page.locator('body')).toContainText('Item created');
  await page.locator('.label-state-private').click();
  await page.locator('#workflow-transition-publish').click();
  await expect(page.locator('body')).toContainText('Item state changed.');
}

async function openTab(page: Page, title: string) {
  await page.locator('.autotoc-nav a', { hasText: title }).click();
}

async function addFolder(page: Page, container: string, title: string) {
  await page.goto(`${container}++add++Folder`);
  await page.locator('#form-widgets-IDublinCore-title').fill(title);
  await saveAndPublish(page);
}

async function addNewsItem(
  page: Page,
  termIds: TermIds,
  title: string,
  site: string,
  image: string,
  category: string,
) {
  await page.goto('portfolio/all-museums/++add++News%20Item');
  await page.locator('#form-widgets-IDublinCore-title').fill(title);
  await page.locator('#form-widgets-IDublinCore-description').fill(site);
  await page
    .locator('input[type=file]')
    .first()
    .setInputFiles(path.join(FIXTURES, image));
  await openTab(page, 'Categorization');
  const options = await page
    .locator(`${CATEGORY_FROM} option`)
    .evaluateAll((nodes) =>
      nodes.map((node) => [
        (node.textContent || '').trim(),
        (node as HTMLOptionElement).value,
      ]),
    );
  for (const [label, value] of options) {
    termIds[label] = value;
  }
  await page.locator(CATEGORY_FROM).selectOption({ label: category });
  await page.locator('button[value="→"]').click();
  await saveAndPublish(page);
}

// The query goes straight into the pat-querystring field: driving the
// select2 criteria widgets by generated ids was brittle, and the widget is
// Plone's, not ours.
async function addCollection(
  page: Page,
  container: string,
  title: string,
  termId: string,
) {
  await page.goto(`${container}++add++Collection`);
  await page.locator('#form-widgets-IDublinCore-title').fill(title);
  const query = JSON.stringify([
    {
      i: 'taxonomy_category',
      o: 'plone.app.querystring.operation.selection.any',
      v: [termId],
    },
  ]);
  await page
    .locator('#form-widgets-ICollection-query')
    .evaluate((node, value) => {
      (node as HTMLInputElement).value = value;
    }, query);
  await openTab(page, 'Settings');
  await page.locator('#form-widgets-IShortName-id').fill('index.html');
  await saveAndPublish(page);
}

async function expectListing(page: Page, shown: string[], hidden: string[]) {
  const content = page.locator('#content');
  for (const title of shown) {
    await expect(content).toContainText(title);
  }
  for (const title of hidden) {
    await expect(content).not.toContainText(title);
  }
}

test('Categorize news items and filter collections by category', async ({
  page,
}) => {
  // One scenario, as the Cypress spec was: each step builds on the content
  // the previous ones created.
  test.setTimeout(240_000);
  const termIds: TermIds = {};

  await test.step('Log in', async () => {
    await login(page);
    await page.goto('');
    await expect(page.locator('body')).toContainText('admin');
  });

  await test.step('Add taxonomy', async () => {
    await page.goto('@@taxonomy-settings');
    await page.locator('#form-buttons-add-taxonomy').click();
    await page.locator('#form-widgets-taxonomy').fill('Category');
    await page
      .locator('#form-widgets-field_description')
      .fill('Categorize your content type');
    await page.locator('#form-widgets-field_title').fill('Category');
    await page.locator('#form-buttons-add').click();
    await expect(page.locator('body')).toContainText('Category');
  });

  await test.step('Add taxonomy data', async () => {
    await page.goto('@@taxonomy-settings');
    // By value, not by index: the example taxonomy installed by the fixture
    // sorts before the one created above.
    await page
      .locator(
        'input[name="form.widgets.taxonomies:list"][value="collective.taxonomy.category"]',
      )
      .check();
    await page.locator('#form-buttons-edit_data_taxonomy').click();
    await page.locator('.tree-view_children > button').click();

    const terms = page.locator('.input-field > input:not(.identifier-input)');
    const inside = page.locator('button[title="Add a term inside this node"]');
    const sibling = page.locator(
      'button[title="Add a node at the same level"]',
    );

    await page.locator('.input-field > input').first().fill('Museums');
    await inside.last().click();
    await terms.last().fill('Netherlands');
    await sibling.last().click();
    await terms.last().fill('France');
    await sibling.last().click();
    await terms.last().fill('England');

    await sibling.first().click();
    await terms.last().fill('Companies');
    await inside.last().click();
    await terms.last().fill('Coca cola');
    await sibling.last().click();
    await terms.last().fill('Pepsi');
    await page.locator('#form-buttons-save').click();
    await expect(page.locator('body')).toContainText(
      'Your taxonomy has been saved with success',
    );
  });

  await test.step('Enable behavior', async () => {
    await page.goto('@@dexterity-types/News%20Item/@@behaviors');
    await page
      .locator('#form-widgets-collective-taxonomy-generated-category-0')
      .check();
    await page.locator('#form-buttons-apply').click();
    await expect(page.locator('body')).toContainText(
      'Behaviors successfully updated.',
    );
  });

  await test.step('Add folders', async () => {
    await addFolder(page, '', 'Portfolio');
    await addFolder(page, 'portfolio/', 'All museums');
    await addFolder(page, 'portfolio/', 'Netherlands Museums');
    await addFolder(page, 'portfolio/', 'France Museums');
  });

  await test.step('Add categorized news items', async () => {
    await addNewsItem(
      page,
      termIds,
      'Centraal Museum',
      'https://www.centraalmuseum.nl/',
      'Centraal_Museum.png',
      'Museums » Netherlands',
    );
    await addNewsItem(
      page,
      termIds,
      'Zeeuws Museum',
      'https://www.zeeuwsmuseum.nl/',
      'Zeeuws_Museum.png',
      'Museums » Netherlands',
    );
    await addNewsItem(
      page,
      termIds,
      'Kunsthal KAdE',
      'http://www.kunsthalkade.nl/',
      'Kunsthal_KAdE.png',
      'Museums » Netherlands',
    );
    await addNewsItem(
      page,
      termIds,
      'Louvre Museum',
      'https://www.louvre.fr',
      'Musee_du_Louvre.png',
      'Museums » France',
    );
  });

  await test.step('Create collections filtering by categories', async () => {
    const all = [
      'Centraal Museum',
      'Zeeuws Museum',
      'Kunsthal KAdE',
      'Louvre Museum',
    ];
    const netherlands = ['Centraal Museum', 'Zeeuws Museum', 'Kunsthal KAdE'];
    const france = ['Louvre Museum'];

    await addCollection(page, 'portfolio/', 'Portfolio', termIds['Museums']);
    await expectListing(page, all, []);

    await addCollection(
      page,
      'portfolio/all-museums/',
      'All Museums',
      termIds['Museums'],
    );
    await expectListing(page, all, []);

    await addCollection(
      page,
      'portfolio/netherlands-museums/',
      'Netherlands Museums',
      termIds['Museums » Netherlands'],
    );
    await expectListing(page, netherlands, france);

    await addCollection(
      page,
      'portfolio/france-museums/',
      'France Museums',
      termIds['Museums » France'],
    );
    await expectListing(page, france, netherlands);
  });
});
