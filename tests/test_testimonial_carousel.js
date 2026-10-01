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
    this.attributes = new Map();
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
  setAttribute(name, value) { this.attributes.set(name, value); }
  getAttribute(name) { return this.attributes.get(name) ?? null; }
  getBoundingClientRect() { return { width: this.width }; }
  scrollBy({ left, behavior }) {
    this.lastScrollBehavior = behavior;
    this.scrollLeft = Math.max(0, Math.min(this.scrollWidth - this.clientWidth, this.scrollLeft + left));
    this.dispatch('scroll');
  }
  scrollTo({ left, behavior }) {
    this.lastScrollBehavior = behavior;
    this.scrollLeft = Math.max(0, Math.min(this.scrollWidth - this.clientWidth, left));
    this.dispatch('scroll');
  }
}

function loadCarousel({ reducedMotion = false } = {}) {
  const track = new FakeElement();
  track.children = Array.from({ length: 12 }, () => new FakeElement({ width: 150 }));
  const previous = new FakeElement();
  const next = new FakeElement();
  const playback = new FakeElement();
  const intervals = new Map();
  let nextIntervalId = 1;
  const markupTags = Array.from(pageMarkup.matchAll(/<(?:div|button)\b[^>]*>/g), ([tag]) => tag);
  const elementsById = new Map();
  const elementsByAttribute = new Map();
  const markupElements = new Map([
    ['data-testimonial-track', track],
    ['data-testimonial-previous', previous],
    ['data-testimonial-next', next],
    ['data-testimonial-playback', playback],
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
  const timers = {
    setInterval(callback, delay) {
      const id = nextIntervalId++;
      intervals.set(id, { callback, delay });
      return id;
    },
    clearInterval(id) { intervals.delete(id); },
  };
  const document = {
    getElementById(id) { return elementsById.get(id) ?? null; },
    querySelector(selector) {
      const attribute = selector.match(/^\[([^\]]+)\]$/)?.[1];
      return attribute ? elementsByAttribute.get(attribute) ?? null : null;
    },
  };
  vm.runInNewContext(appScript, { Array, document, window, ...timers }, { filename: 'script.js' });
  return {
    track,
    previous,
    next,
    playback,
    tick() { for (const interval of intervals.values()) interval.callback(); },
    intervalDelays() { return Array.from(intervals.values(), ({ delay }) => delay); },
  };
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

test('testimonial controls place an accessible playback toggle between previous and next', () => {
  const controls = pageMarkup.match(/<div class="testimonial-controls"[^>]*>([\s\S]*?)<\/div>/)?.[1] ?? '';
  const buttons = Array.from(controls.matchAll(/<button\b[^>]*>/g), ([button]) => button);

  assert.equal(buttons.length, 3);
  assert.match(buttons[0], /data-testimonial-previous/);
  assert.match(buttons[1], /data-testimonial-playback/);
  assert.match(buttons[1], /aria-label="Pausar reproducción automática"/);
  assert.match(buttons[1], /aria-pressed="true"/);
  assert.match(buttons[2], /data-testimonial-next/);
});

test('carousel advances automatically, pauses, and resumes on demand', () => {
  const { track, playback, tick, intervalDelays } = loadCarousel();

  assert.deepEqual(intervalDelays(), [5000]);
  tick();
  assert.equal(track.scrollLeft, 166);

  playback.dispatch('click');
  assert.deepEqual(intervalDelays(), []);
  assert.equal(playback.getAttribute('aria-label'), 'Reanudar reproducción automática');
  tick();
  assert.equal(track.scrollLeft, 166);

  playback.dispatch('click');
  assert.deepEqual(intervalDelays(), [5000]);
  assert.equal(playback.getAttribute('aria-label'), 'Pausar reproducción automática');
});

test('carousel autoplay loops back to the first testimonial at the end', () => {
  const { track, tick } = loadCarousel();
  track.scrollLeft = track.scrollWidth - track.clientWidth;
  track.dispatch('scroll');

  tick();

  assert.equal(track.scrollLeft, 0);
});

test('reduced motion starts paused but lets the reader explicitly resume playback', () => {
  const { track, playback, tick, intervalDelays } = loadCarousel({ reducedMotion: true });

  assert.deepEqual(intervalDelays(), []);
  assert.equal(playback.getAttribute('aria-label'), 'Reanudar reproducción automática');
  tick();
  assert.equal(track.scrollLeft, 0);

  playback.dispatch('click');
  assert.deepEqual(intervalDelays(), [5000]);
  tick();
  assert.equal(track.scrollLeft, 166);
});
