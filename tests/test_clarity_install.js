const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

test('head bootstraps the configured Clarity project without blocking page load', () => {
  const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
  const head = html.match(/<head>([\s\S]*?)<\/head>/i)?.[1];
  assert.ok(head, 'the page must have a head');

  const inlineScripts = [...head.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi)]
    .filter((match) => match[1].trim());
  assert.equal(inlineScripts.length, 1, 'the Clarity bootstrap must be inline in the head');

  let insertedScript;
  const firstScript = {
    parentNode: {
      insertBefore(script, reference) {
        assert.equal(reference, firstScript);
        insertedScript = script;
      },
    },
  };
  const document = {
    createElement(tag) {
      assert.equal(tag, 'script');
      return {};
    },
    getElementsByTagName(tag) {
      assert.equal(tag, 'script');
      return [firstScript];
    },
  };
  const window = {};

  vm.runInNewContext(inlineScripts[0][1], { window, document });

  assert.equal(insertedScript.src, 'https://www.clarity.ms/tag/yp14daof19');
  assert.equal(insertedScript.async, 1);
  window.clarity('event', 'purchase-cta');
  assert.deepEqual(Array.from(window.clarity.q[0]), ['event', 'purchase-cta']);
});
