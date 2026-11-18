import type { APIRequestContext, Page } from '@playwright/test';

import { basicAuthHeader, getApiURL, SITE_OWNER } from './config';

export type CreateContentParams = {
  contentType: string;
  contentId: string;
  contentTitle: string;
  contentDescription?: string;
  path?: string;
  transition?: string;
  bodyModifier?: (body: Record<string, unknown>) => Record<string, unknown>;
};

function getRequestContext(requestOrPage: APIRequestContext | Page) {
  if ('request' in requestOrPage) return requestOrPage.request;
  return requestOrPage;
}

function normalizePath(value?: string) {
  if (!value) return '';
  return value.replace(/^\/+/, '').replace(/\/+$/, '');
}

/**
 * Creates content through the REST API, as the site owner.
 *
 * Unlike the Volto template's helper, it sends no blocks: the Classic UI
 * content types do not have them.
 */
export async function createContent(
  requestOrPage: APIRequestContext | Page,
  {
    contentType,
    contentId,
    contentTitle,
    contentDescription = '',
    path = '',
    transition = '',
    bodyModifier = (body) => body,
  }: CreateContentParams,
) {
  const request = getRequestContext(requestOrPage);
  const apiURL = getApiURL();
  const authHeader = basicAuthHeader(...SITE_OWNER);
  const normalizedPath = normalizePath(path);
  const containerUrl = `${apiURL}/${normalizedPath}`;

  const body = bodyModifier({
    '@type': contentType,
    id: contentId,
    title: contentTitle,
    description: contentDescription,
  });

  const response = await request.post(containerUrl, {
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      Authorization: authHeader,
    },
    data: body,
  });

  if (!response.ok()) {
    throw new Error(
      `Create content failed: POST ${containerUrl} returned ${response.status()} ${response.statusText()}`,
    );
  }

  if (transition) {
    const prefix = normalizedPath ? `${normalizedPath}/` : '';
    const url = `${apiURL}/${prefix}${normalizePath(contentId)}/@workflow/${transition}`;

    const transitionResponse = await request.post(url, {
      headers: {
        Accept: 'application/json',
        Authorization: authHeader,
      },
    });

    if (!transitionResponse.ok()) {
      throw new Error(
        `Workflow transition failed: POST ${url} returned ${transitionResponse.status()} ${transitionResponse.statusText()}`,
      );
    }
  }

  return response;
}
