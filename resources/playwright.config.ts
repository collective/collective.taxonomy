import { defineConfig, devices } from '@playwright/test';

import { getApiURL } from './acceptance/tests/config';

// Acceptance tests run against the Plone acceptance fixture started by
// `make acceptance-backend-start` (robot-server, with RobotRemote enabled so
// the backend can be reset between tests). The Classic UI is served by the
// same fixture, so there is no separate frontend.
export default defineConfig({
  testDir: 'acceptance/tests',
  testMatch: ['**/*.{spec,test}.{ts,tsx}'],
  outputDir: 'acceptance/results',
  // Disable parallel tests to avoid conflicts creating/deleting content while
  // sharing a single backend that is reset between tests.
  workers: 1,
  // Fail the build on CI if you accidentally left test.only in the source code.
  forbidOnly: !!process.env.CI,
  // Retry on CI only.
  retries: process.env.CI ? 3 : 0,
  timeout: 30_000,
  expect: {
    timeout: 10_000,
  },
  use: {
    // Trailing slash: tests navigate with paths relative to the site.
    baseURL: `${getApiURL()}/`,
    browserName: 'chromium',
    viewport: { width: 1440, height: 1000 },
    trace: 'retain-on-failure',
    // Use video only while debugging CI
    // video: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        viewport: { width: 1440, height: 1000 },
      },
    },
  ],
});
