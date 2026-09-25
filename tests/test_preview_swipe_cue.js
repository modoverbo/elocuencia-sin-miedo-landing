const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const appScript = fs.readFileSync(path.join(__dirname, '..', 'script.js'), 'utf8');

class FakeElement {
  constructor() {
    this.attributes = new Map();
    const classes = new Set();
    this.classList = {
      add: (...names) => names.forEach((name) => classes.add(name)),
      remove: (...names) => names.forEach((name) => classes.delete(name)),
      contains: (name) => classes.has(name),
      has: (name) => classes.has(name),
    };
    this.listeners = new Map();
    this.disabled = false;
    this.hidden = false;
    this.innerHTML = '';
    this.textContent = '';
    this.open = false;
  }

  addEventListener(type, listener) {
    const listeners = this.listeners.get(type) ?? [];
    listeners.push(listener);
    this.listeners.set(type, listeners);
  }

  dispatch(type, properties = {}) {
    for (const listener of this.listeners.get(type) ?? []) {
      listener({ target: this, ...properties });
    }
  }

  querySelectorAll() {
    return [];
  }

  setAttribute(name, value) {
    this.attributes.set(name, value);
  }
}

class FakePageFlip {
  on() {}
  loadFromHTML() {}
  getCurrentPageIndex() { return 0; }
  getOrientation() { return 'portrait'; }
  getSettings() { return {}; }
  flipNext() {}
  flipPrev() {}
  turnToPage() {}
}

function loadPreview({ reducedMotion = false } = {}) {
  const elements = new Map();
  const document = {
    getElementById(id) {
      if (!elements.has(id)) elements.set(id, new FakeElement());
      return elements.get(id);
    },
    addEventListener() {},
  };
  const motionPreference = {
    matches: reducedMotion,
    listener: null,
    addEventListener(_type, listener) { this.listener = listener; },
  };
  const window = {
    St: { PageFlip: FakePageFlip },
    matchMedia: () => motionPreference,
  };
  document.getElementById('preview-swipe-cue');
  const context = {
    Array,
    Math,
    St: window.St,
    document,
    performance: { now: () => 0 },
    requestAnimationFrame: (callback) => callback(),
    window,
  };

  vm.runInNewContext(appScript, context, { filename: 'script.js' });
  return {
    book: elements.get('flipbook'),
    cue: elements.get('preview-swipe-cue'),
    mediaPreference: motionPreference,
  };
}

test('starts the cue once and dismisses it on the first preview pointer interaction', () => {
  const { book, cue } = loadPreview();

  assert.equal(cue.classList.has('is-animated'), true);
  assert.equal(cue.classList.has('is-dismissed'), false);

  book.dispatch('pointerdown', { pointerId: 1, clientX: 40, clientY: 60 });

  assert.equal(cue.classList.has('is-animated'), false);
  assert.equal(cue.classList.has('is-dismissed'), true);

  book.dispatch('pointerdown', { pointerId: 2, clientX: 50, clientY: 65 });
  assert.equal(cue.classList.has('is-animated'), false);
});

test('respects reduced motion at load and stops if the preference changes mid-cue', () => {
  const reducedAtLoad = loadPreview({ reducedMotion: true });
  assert.equal(reducedAtLoad.cue.classList.has('is-animated'), false);
  assert.equal(reducedAtLoad.cue.classList.has('is-dismissed'), false);

  const changedDuringCue = loadPreview();
  assert.equal(changedDuringCue.cue.classList.has('is-animated'), true);
  changedDuringCue.mediaPreference.matches = true;
  changedDuringCue.mediaPreference.listener({ matches: true });
  assert.equal(changedDuringCue.cue.classList.has('is-animated'), false);
  assert.equal(changedDuringCue.cue.classList.has('is-dismissed'), true);
});
