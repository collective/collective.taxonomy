import type { Page } from '@playwright/test';

import { createContent } from './content';
import { login } from './login';
import { expect, test } from './test';

// The example taxonomy (collective.taxonomy:examples) installed by the
// acceptance fixture.
const BEHAVIOR_CHECKBOX =
  'input[name="form.widgets.collective.taxonomy.generated.test:list"]';
const FROM = 'select[name="form.widgets.test.taxonomy_test.from"]';
const TO = 'select[name="form.widgets.test.taxonomy_test.to"]';

const PAGE_ID = 'an-edited-page';

async function editPage(page: Page) {
  await page.goto(`${PAGE_ID}/edit`);
  await expect(page.locator('body')).toContainText('Edit Page');
}

async function selectTerm(page: Page, label: string) {
  await page.locator(FROM).selectOption({ label });
  await page.locator('button[name="from2toButton"]').click();
}

async function deselectTerm(page: Page, label: string) {
  await page.locator(TO).selectOption({ label });
  await page.locator('button[name="to2fromButton"]').click();
}

test('As a manager I can select and deselect taxonomy terms', async ({
  page,
}) => {
  await login(page);
  await createContent(page, {
    contentType: 'Document',
    contentId: PAGE_ID,
    contentTitle: 'An edited page',
  });

  await page.goto('dexterity-types/Document/@@behaviors');
  await page.locator(BEHAVIOR_CHECKBOX).check();
  await page.locator('button[name="form.buttons.apply"]').click();
  await expect(page.locator('body')).toContainText(
    'Behaviors successfully updated.',
  );

  await editPage(page);
  await selectTerm(page, 'Information Science');
  await selectTerm(page, 'Information Science » Chronology');
  await expect(page.locator(`${TO} option`)).toHaveCount(2);

  await page.locator('button[name="form.buttons.save"]').click();
  await expect(page.locator('body')).toContainText('Changes saved');

  await editPage(page);
  await deselectTerm(page, 'Information Science');
  await expect(page.locator(`${TO} option`)).toHaveCount(1);
});
