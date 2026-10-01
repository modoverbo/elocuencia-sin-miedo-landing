const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const appScript = fs.readFileSync(path.join(root, 'script.js'), 'utf8');

test('literal reference layout does not introduce a post-hero sticky purchase bar', () => {
  assert.doesNotMatch(html, /post-hero-buy|post-hero-purchase-cta/);
  assert.doesNotMatch(appScript, /post-hero-buy|updatePurchaseBar/);
});
