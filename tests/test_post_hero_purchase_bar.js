const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const appScript = fs.readFileSync(path.join(__dirname, '..', 'script.js'), 'utf8');

class FakeElement {
  constructor(id, document) {
    this.id = id;
    this.document = document;
    this.hidden = id === 'post-hero-buy';
    this.inert = id === 'post-hero-buy';
    this.attributes = new Map(id === 'post-hero-buy' ? [['aria-hidden', 'true']] : []);
    this.listeners = new Map();
    this.children = new Set();
    this.classList = { toggle() {} };
    this.bounds = { top: 1200, bottom: 1300 };
  }

  addEventListener(type, callback) {
    const listeners = this.listeners.get(type) ?? [];
    listeners.push(callback);
    this.listeners.set(type, listeners);
  }

  setAttribute(name, value) { this.attributes.set(name, value); }
  contains(element) { return this.children.has(element); }
  focus(options) {
    this.focusOptions = options;
    this.document.activeElement = this;
  }
  getBoundingClientRect() { return this.bounds; }
}

function loadLandingBar({ intersectionObserver = true } = {}) {
  const elements = new Map();
  const windowListeners = new Map();
  const document = {
    activeElement: null,
    getElementById(id) {
      if (!elements.has(id)) elements.set(id, new FakeElement(id, document));
      return elements.get(id);
    },
  };
  const hero = document.getElementById('inicio');
  const bar = document.getElementById('post-hero-buy');
  const previewControls = document.getElementById('preview-controls');
  const footer = document.getElementById('site-footer');
  const heroCta = document.getElementById('hero-purchase-cta');
  const barCta = document.getElementById('post-hero-purchase-cta');
  const previewNext = document.getElementById('preview-next');
  const footerCta = document.getElementById('footer-purchase-cta');
  bar.children.add(barCta);
  const observers = [];

  class FakeIntersectionObserver {
    constructor(callback, options) {
      this.callback = callback;
      this.options = options;
      this.targets = new Set();
      observers.push(this);
    }

    observe(target) { this.targets.add(target); }
    trigger(target, isIntersecting) {
      this.callback([{ target, isIntersecting }], this);
    }
  }

  const window = {
    innerHeight: 800,
    matchMedia: () => ({ matches: false, addEventListener() {} }),
    addEventListener(type, callback) {
      const listeners = windowListeners.get(type) ?? [];
      listeners.push(callback);
      windowListeners.set(type, listeners);
    },
    removeEventListener(type, callback) {
      windowListeners.set(type, (windowListeners.get(type) ?? []).filter((item) => item !== callback));
    },
    dispatch(type) {
      for (const callback of windowListeners.get(type) ?? []) callback();
    },
  };
  if (intersectionObserver) window.IntersectionObserver = FakeIntersectionObserver;

  const context = { Array, document, window };
  vm.runInNewContext(appScript, context, { filename: 'script.js' });
  return { bar, barCta, footer, footerCta, hero, heroCta, observers, previewControls, previewNext, window };
}

test('purchase bar starts hidden, appears after hero exit, and yields to preview controls and footer', () => {
  const { bar, footer, hero, observers, previewControls } = loadLandingBar();
  assert.equal(bar.hidden, true);
  assert.equal(bar.inert, true);
  assert.equal(bar.attributes.get('aria-hidden'), 'true');
  assert.equal(observers.length, 1);
  assert.deepEqual([...observers[0].targets], [hero, previewControls, footer]);

  observers[0].trigger(hero, false);
  assert.equal(bar.hidden, true, 'wait until protected regions have initial visibility state');
  observers[0].trigger(previewControls, false);
  observers[0].trigger(footer, false);
  assert.equal(bar.hidden, false);
  assert.equal(bar.inert, false);
  assert.equal(bar.attributes.get('aria-hidden'), 'false');

  observers[0].trigger(previewControls, true);
  assert.equal(bar.hidden, true);
  observers[0].trigger(previewControls, false);
  assert.equal(bar.hidden, false);
  observers[0].trigger(footer, true);
  assert.equal(bar.hidden, true);
});

test('reverse scroll hides the bar and transfers focus from its CTA to the hero CTA', () => {
  const { bar, barCta, footer, hero, heroCta, observers, previewControls } = loadLandingBar();
  const observer = observers[0];
  observer.trigger(previewControls, false);
  observer.trigger(footer, false);
  observer.trigger(hero, false);
  barCta.focus();

  observer.trigger(hero, true);

  assert.equal(bar.hidden, true);
  assert.equal(bar.inert, true);
  assert.equal(heroCta.document.activeElement, heroCta);
  assert.equal(heroCta.focusOptions.preventScroll, true);
});

test('focused bar action moves to the visible region checkout or preview action when suppressed', () => {
  const { barCta, footerCta, observers, previewNext } = loadLandingBar();
  const observer = observers[0];
  observer.trigger(documentElement(observer, 'preview-controls'), false);
  observer.trigger(documentElement(observer, 'site-footer'), false);
  observer.trigger(documentElement(observer, 'inicio'), false);
  barCta.focus();
  observer.trigger(documentElement(observer, 'preview-controls'), true);
  assert.equal(previewNext.document.activeElement, previewNext);

  observer.trigger(documentElement(observer, 'preview-controls'), false);
  observer.trigger(documentElement(observer, 'site-footer'), false);
  observer.trigger(documentElement(observer, 'inicio'), false);
  barCta.focus();
  observer.trigger(documentElement(observer, 'site-footer'), true);
  assert.equal(footerCta.document.activeElement, footerCta);
});

function documentElement(observer, id) {
  return [...observer.targets].find((element) => element.id === id);
}

test('scroll and resize fallback preserve hero and protected-region visibility behavior', () => {
  const { bar, footer, hero, previewControls, window } = loadLandingBar({ intersectionObserver: false });
  hero.bounds = { top: -1000, bottom: -50 };
  previewControls.bounds = { top: 900, bottom: 940 };
  footer.bounds = { top: 2000, bottom: 2500 };
  window.dispatch('scroll');
  assert.equal(bar.hidden, false);

  previewControls.bounds = { top: 770, bottom: 795 };
  window.dispatch('resize');
  assert.equal(bar.hidden, true);

  hero.bounds = { top: 0, bottom: 500 };
  previewControls.bounds = { top: 900, bottom: 940 };
  window.dispatch('scroll');
  assert.equal(bar.hidden, true);
});
