import type { APIRequestContext, Page } from '@playwright/test';

import { getApiURL } from './config';

function getRequestContext(requestOrPage: APIRequestContext | Page) {
  if ('request' in requestOrPage) return requestOrPage.request;
  return requestOrPage;
}

const ROBOT_HEADERS = { Accept: 'text/xml', 'content-type': 'text/xml' };

// The acceptance backend is started with this package's acceptance layer
// (see `make acceptance-backend-start`), so we reset the ZODB to that layer's
// baseline between tests via RobotRemote.
const TESTING_LAYER = 'collective.taxonomy.testing.ACCEPTANCE_TESTING';

const SETUP_BODY = `<?xml version="1.0"?><methodCall><methodName>run_keyword</methodName><params><param><value><string>remote_zodb_setup</string></value></param><param><value><array><data><value><string>${TESTING_LAYER}</string></value></data></array></value></param></params></methodCall>`;

const TEARDOWN_BODY = `<?xml version="1.0"?><methodCall><methodName>run_keyword</methodName><params><param><value><string>remote_zodb_teardown</string></value></param><param><value><array><data><value><string>${TESTING_LAYER}</string></value></data></array></value></param></params></methodCall>`;

async function callRobotRemote(
  request: APIRequestContext,
  apiURL: string,
  body: string,
) {
  const url = `${apiURL}/RobotRemote`;
  const response = await request.post(url, {
    headers: ROBOT_HEADERS,
    data: body,
  });

  if (!response.ok()) {
    throw new Error(
      `RobotRemote call failed: POST ${url} returned ${response.status()} ${response.statusText()}`,
    );
  }

  return response;
}

export async function setup(
  requestOrPage: APIRequestContext | Page,
  apiURL: string = getApiURL(),
) {
  const request = getRequestContext(requestOrPage);
  return callRobotRemote(request, apiURL, SETUP_BODY);
}

export async function teardown(
  requestOrPage: APIRequestContext | Page,
  apiURL: string = getApiURL(),
) {
  const request = getRequestContext(requestOrPage);
  return callRobotRemote(request, apiURL, TEARDOWN_BODY);
}
