const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const appScript = fs.readFileSync(path.join(__dirname, '..', 'script.js'), 'utf8');
const pageMarkup = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');

class FakeElement {
  constructor({ width = 0 } = {}) {
    this.disabled = false;
    this.listeners = new Map();
    this.scrollLeft = 0;
    this.scrollWidth = 2400;
    this.clientWidth = 800;
    this.width = width;
    this.children = [];
  }

  addEventListener(type, listener) {
    const listeners = this.listeners.get(type) ?? [];
    listeners.push(listener);
    this.listeners.set(type, listeners);
  }

  dispatch(type, properties = {}) {
    for (const listener of this.listeners.get(type) ?? []) {
      listener({ target: this, preventDefault() { this.defaultPrevented = true; }, ...properties });
    }
  }

  querySelectorAll() { return this.children; }
  getBoundingClientRect() { return { width: this.width }; }
  scrollBy({ left, behavior }) {
    this.lastScrollBehavior = behavior;
    this.scrollLeft = Math.max(0, Math.min(this.scrollWidth - this.clientWidth, this.scrollLeft + left));
    this.dispatch('scroll');
  }
}

function loadCarousel({ reducedMotion = false } = {}) {
  const track = new FakeElement();
  track.children = Array.from({ length: 12 }, () => new FakeElement({ width: 150 }));
  const previous = new FakeElement();
  const next = new FakeElement();
  const markupTags = Array.from(pageMarkup.matchAll(/<(?:div|button)\b[^>]*>/g), ([tag]) => tag);
  const elementsById = new Map();
  const elementsByAttribute = new Map();
  const markupElements = new Map([
    ['data-testimonial-track', track],
    ['data-testimonial-previous', previous],
    ['data-testimonial-next', next],
  ]);
  markupTags.forEach((tag) => {
    const id = tag.match(/\bid="([^"]+)"/)?.[1];
    if (id && tag.includes('data-testimonial-track')) elementsById.set(id, track);
    for (const attribute of markupElements.keys()) {
      if (tag.includes(attribute)) elementsByAttribute.set(attribute, markupElements.get(attribute));
    }
  });
  const window = {
    matchMedia: () => ({ matches: reducedMotion }),
    getComputedStyle: () => ({ columnGap: '16px', gap: '16px' }),
    addEventListener() {},
  };
  const document = {
    getElementById(id) { return elementsById.get(id) ?? null; },
    querySelector(selector) {
      const attribute = selector.match(/^\[([^\]]+)\]$/)?.[1];
      return attribute ? elementsByAttribute.get(attribute) ?? null : null;
    },
  };
  vm.runInNewContext(appScript, { Array, document, window }, { filename: 'script.js' });
  return { track, previous, next };
}

test('carousel controls and arrow keys move by card and keep edge controls disabled', () => {
  const { track, previous, next } = loadCarousel();

  assert.equal(previous.disabled, true);
  assert.equal(next.disabled, false);
  track.dispatch('keydown', { key: 'ArrowRight' });
  assert.equal(track.scrollLeft, 166);
  assert.equal(previous.disabled, false);
  assert.equal(track.lastScrollBehavior, 'smooth');

  previous.dispatch('click');
  assert.equal(track.scrollLeft, 0);
  assert.equal(previous.disabled, true);

  track.dispatch('keydown', { key: 'ArrowLeft' });
  assert.equal(track.scrollLeft, 0);
  next.dispatch('click');
  assert.equal(track.scrollLeft, 166);
});

test('carousel avoids smooth scrolling when reduced motion is requested', () => {
  const { track } = loadCarousel({ reducedMotion: true });

  track.dispatch('keydown', { key: 'ArrowRight' });

  assert.equal(track.lastScrollBehavior, 'auto');
  assert.equal(track.scrollLeft, 166);
});
