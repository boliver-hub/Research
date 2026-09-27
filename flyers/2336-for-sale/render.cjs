// Renders flyer.html to a print-ready Letter PDF and a PNG preview.
// Usage: node render.cjs   (requires the `playwright` package and a Chromium build)
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const dir = __dirname;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 816, height: 1056 }, deviceScaleFactor: 2 });
  await page.goto('file://' + path.join(dir, 'flyer.html'), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);

  await page.pdf({ path: path.join(dir, 'flyer.pdf'), format: 'Letter', printBackground: true, preferCSSPageSize: true });

  await page.emulateMedia({ media: 'print' });
  await page.locator('.page').screenshot({ path: path.join(dir, 'flyer-preview.png') });

  await browser.close();
})();
