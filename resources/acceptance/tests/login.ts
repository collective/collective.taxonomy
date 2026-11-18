import type { Page } from '@playwright/test';

import { basicAuthHeader, SITE_OWNER } from './config';

export type LoginOptions = {
  username?: string;
  password?: string;
};

/**
 * Logs in to the Classic UI.
 *
 * Plone accepts HTTP Basic authentication on every request, so the browser
 * context sends the credentials with each page load and each request the
 * page makes (the taxonomy editor's fetch calls included). This replaces the
 * Volto template's `auth_token` cookie, which the Classic UI does not read.
 */
export async function login(page: Page, options: LoginOptions = {}) {
  const username = options.username || SITE_OWNER[0];
  const password = options.password || SITE_OWNER[1];
  await page.context().setExtraHTTPHeaders({
    Authorization: basicAuthHeader(username, password),
  });
}
