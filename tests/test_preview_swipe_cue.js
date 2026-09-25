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

function loadPreview({ reducedMotion = false, intersectionObserver = true, bookTop = 1200 } = {}) {
  const elements = new Map();
  const windowListeners = new Map();
  const visibility = { observer: null };
  class FakeIntersectionObserver {
    constructor(callback, options) {
      this.callback = callback;
      this.options = options;
      this.observed = null;
      this.unobserved = null;
      visibility.observer = this;
    }

    observe(target) { this.observed = target; }
    unobserve(target) { this.unobserved = target; }
    disconnect() { this.disconnected = true; }
    trigger(isIntersecting = true) {
      this.callback([{ target: this.observed, isIntersecting }], this);
    }
  }
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
    innerHeight: 800,
    addEventListener(type, listener) {
      const listeners = windowListeners.get(type) ?? [];
      listeners.push(listener);
      windowListeners.set(type, listeners);
    },
    removeEventListener(type, listener) {
      windowListeners.set(type, (windowListeners.get(type) ?? []).filter((item) => item !== listener));
    },
    dispatch(type) {
      for (const listener of windowListeners.get(type) ?? []) listener();
    },
  };
  if (intersectionObserver) window.IntersectionObserver = FakeIntersectionObserver;
  document.getElementById('preview-swipe-cue');
  document.getElementById('flipbook').getBoundingClientRect = () => ({ top: bookTop, bottom: bookTop + 480 });
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
    observer: visibility.observer,
    setBookTop(top) { bookTop = top; },
    window,
  };
}

test('waits for the preview to enter view, then dismisses the cue on first pointer interaction', () => {
  const { book, cue, observer } = loadPreview();

  assert.equal(cue.classList.has('is-animated'), false);
  assert.equal(cue.classList.has('is-dismissed'), false);
  assert.equal(observer.observed, book);
  observer.trigger();
  assert.equal(cue.classList.has('is-animated'), true);
  assert.equal(observer.disconnected, true);

  book.dispatch('pointerdown', { pointerId: 1, clientX: 40, clientY: 60 });

  assert.equal(cue.classList.has('is-animated'), false);
  assert.equal(cue.classList.has('is-dismissed'), true);

  book.dispatch('pointerdown', { pointerId: 2, clientX: 50, clientY: 65 });
  assert.equal(cue.classList.has('is-animated'), false);
});

test('does not animate under reduced motion at load or after preference changes before visibility', () => {
  const reducedAtLoad = loadPreview({ reducedMotion: true });
  assert.equal(reducedAtLoad.cue.classList.has('is-animated'), false);
  assert.equal(reducedAtLoad.cue.classList.has('is-dismissed'), false);

  const changedBeforeVisibility = loadPreview();
  assert.equal(changedBeforeVisibility.cue.classList.has('is-animated'), false);
  changedBeforeVisibility.mediaPreference.matches = true;
  changedBeforeVisibility.mediaPreference.listener({ matches: true });
  changedBeforeVisibility.observer.trigger();
  assert.equal(changedBeforeVisibility.cue.classList.has('is-animated'), false);
  assert.equal(changedBeforeVisibility.observer.disconnected, true);
});

test('fallback waits for the book to enter the viewport when IntersectionObserver is unavailable', () => {
  const { book, cue, setBookTop, window } = loadPreview({ intersectionObserver: false });
  assert.equal(cue.classList.has('is-animated'), false);

  setBookTop(300);
  window.dispatch('scroll');

  assert.equal(cue.classList.has('is-animated'), true);
  book.dispatch('pointerdown', { pointerId: 1, clientX: 40, clientY: 60 });
  assert.equal(cue.classList.has('is-animated'), false);
});
