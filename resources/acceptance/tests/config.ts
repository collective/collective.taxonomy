/**
 * Where the acceptance backend lives, and who to log in as.
 *
 * The defaults match `make acceptance-backend-start`. Override them with
 * `BACKEND_HOST`, `SITE_ID` or `API_PATH`.
 */
export function getApiURL(): string {
  const hostname = process.env.BACKEND_HOST || '127.0.0.1';
  const siteId = process.env.SITE_ID || 'plone';
  return process.env.API_PATH || `http://${hostname}:55001/${siteId}`;
}

/** The site owner of the plone.app.testing fixture. */
export const SITE_OWNER: [string, string] = ['admin', 'secret'];

export function basicAuthHeader(username: string, password: string): string {
  const token = Buffer.from(`${username}:${password}`, 'utf8').toString(
    'base64',
  );
  return `Basic ${token}`;
}
