(() => {
  'use strict';

  const byId = (id) => document.getElementById(id);

  function setupTestimonialCarousel() {
    const track = byId('testimonial-track');
    const previous = document.querySelector('[data-testimonial-previous]');
    const next = document.querySelector('[data-testimonial-next]');
    const playback = document.querySelector('[data-testimonial-playback]');
    if (!track || !previous || !next || !playback) return;

    const cards = Array.from(track.querySelectorAll('.testimonial'));
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    const autoplayDelay = 5000;
    let autoplayTimer = null;

    function updateControls() {
      const maximumScroll = Math.max(0, Number(track.scrollWidth || 0) - Number(track.clientWidth || 0));
      previous.disabled = track.scrollLeft <= 1;
      next.disabled = maximumScroll <= 1 || track.scrollLeft >= maximumScroll - 1;
    }

    function scrollByCard(direction) {
      if (!cards.length) return;
      const cardWidth = cards[0].getBoundingClientRect().width || track.clientWidth || 320;
      const gap = window.getComputedStyle
        ? Number.parseFloat(window.getComputedStyle(track).columnGap || window.getComputedStyle(track).gap) || 16
        : 16;
      const distance = (cardWidth + gap) * direction;
      if (track.scrollBy) {
        track.scrollBy({ left: distance, behavior: reducedMotion.matches ? 'auto' : 'smooth' });
      } else {
        track.scrollLeft += distance;
      }
      updateControls();
    }

    function updatePlaybackControl(isPlaying) {
      playback.setAttribute('aria-label', isPlaying
        ? 'Pausar reproducción automática'
        : 'Reanudar reproducción automática');
      playback.setAttribute('aria-pressed', String(isPlaying));
      playback.textContent = isPlaying ? 'Ⅱ' : '▶';
    }

    function advanceAutomatically() {
      const maximumScroll = Math.max(0, Number(track.scrollWidth || 0) - Number(track.clientWidth || 0));
      if (maximumScroll > 1 && track.scrollLeft >= maximumScroll - 1) {
        if (track.scrollTo) {
          track.scrollTo({ left: 0, behavior: reducedMotion.matches ? 'auto' : 'smooth' });
        } else {
          track.scrollLeft = 0;
        }
        updateControls();
        return;
      }
      scrollByCard(1);
    }

    function stopAutoplay() {
      if (autoplayTimer !== null) clearInterval(autoplayTimer);
      autoplayTimer = null;
      updatePlaybackControl(false);
    }

    function startAutoplay() {
      if (autoplayTimer !== null || cards.length < 2) return;
      autoplayTimer = setInterval(advanceAutomatically, autoplayDelay);
      updatePlaybackControl(true);
    }

    previous.addEventListener('click', () => scrollByCard(-1));
    next.addEventListener('click', () => scrollByCard(1));
    playback.addEventListener('click', () => {
      if (autoplayTimer === null) startAutoplay();
      else stopAutoplay();
    });
    track.addEventListener('scroll', updateControls, { passive: true });
    track.addEventListener('keydown', (event) => {
      if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
      event.preventDefault();
      scrollByCard(event.key === 'ArrowRight' ? 1 : -1);
    });
    window.addEventListener('resize', updateControls);
    updateControls();
    if (reducedMotion.matches) updatePlaybackControl(false);
    else startAutoplay();
  }

  setupTestimonialCarousel();

  const bookElement = byId('flipbook');
  if (!bookElement) return;

  const TOTAL_PAGES = 156;
  const PREVIEW_LAST_PAGE = 14;
  const counter = byId('preview-counter');
  const previous = byId('preview-previous');
  const next = byId('preview-next');
  const replay = byId('preview-replay');
  const end = byId('preview-end');
  const zoom = byId('page-zoom');
  const zoomImage = byId('zoom-image');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const swipeCue = byId('preview-swipe-cue');
  let swipeCueState = swipeCue ? (reducedMotion.matches ? 'suppressed' : 'pending') : 'disabled';
  let swipeCueObserver = null;
  let swipeCueFallbackCheck = null;

  function stopSwipeCue() {
    if (swipeCueState !== 'pending' && swipeCueState !== 'active') return;
    swipeCueState = 'dismissed';
    swipeCue.classList.remove('is-animated');
    swipeCue.classList.add('is-dismissed');
    removeSwipeCueVisibilityWatch();
  }

  function removeSwipeCueVisibilityWatch() {
    if (swipeCueObserver) {
      swipeCueObserver.disconnect();
      swipeCueObserver = null;
    }
    if (swipeCueFallbackCheck) {
      window.removeEventListener('scroll', swipeCueFallbackCheck);
      window.removeEventListener('resize', swipeCueFallbackCheck);
      swipeCueFallbackCheck = null;
    }
  }

  function updateSwipeCueVisibility(isVisible) {
    if (swipeCueState !== 'pending' && swipeCueState !== 'active') return;
    if (reducedMotion.matches) {
      swipeCueState = 'suppressed';
      removeSwipeCueVisibilityWatch();
      return;
    }
    swipeCueState = isVisible ? 'active' : 'pending';
    swipeCue.classList.toggle('is-animated', isVisible);
  }

  function watchSwipeCueVisibility() {
    if (swipeCueState !== 'pending') return;
    if (window.IntersectionObserver) {
      swipeCueObserver = new window.IntersectionObserver((entries) => {
        const entry = entries.find((item) => item.target === bookElement);
        if (entry) updateSwipeCueVisibility(entry.isIntersecting);
      }, { threshold: 0.15 });
      swipeCueObserver.observe(bookElement);
      return;
    }

    swipeCueFallbackCheck = () => {
      const bounds = bookElement.getBoundingClientRect();
      const viewportBottom = window.innerHeight || document.documentElement.clientHeight;
      updateSwipeCueVisibility(bounds.bottom > 0 && bounds.top < viewportBottom);
    };
    window.addEventListener('scroll', swipeCueFallbackCheck);
    window.addEventListener('resize', swipeCueFallbackCheck);
    swipeCueFallbackCheck();
  }

  if (!window.St || !St.PageFlip) {
    counter.textContent = 'Muestra temporalmente no disponible';
    previous.disabled = true;
    next.disabled = true;
    return;
  }

  const pages = Array.from(bookElement.querySelectorAll('.preview-page, .preview-lock-page'));
  const pageFlip = new St.PageFlip(bookElement, {
    width: 360,
    height: 480,
    size: 'stretch',
    minWidth: 220,
    maxWidth: 360,
    minHeight: 293,
    maxHeight: 480,
    autoSize: false,
    usePortrait: true,
    showCover: true,
    drawShadow: true,
    maxShadowOpacity: 0.38,
    flippingTime: reducedMotion.matches ? 120 : 760,
    mobileScrollSupport: true,
    swipeDistance: 24,
    clickEventForward: true,
    disableFlipByClick: true,
  });

  let isFlipping = false;
  let pointerStart = null;
  let suppressZoomUntil = 0;

  function finishPreview() {
    const atEnd = pageFlip.getCurrentPageIndex() >= PREVIEW_LAST_PAGE - 1;
    end.hidden = !(atEnd && pageFlip.getOrientation() === 'portrait');
    next.disabled = atEnd || isFlipping;
    if (atEnd) next.setAttribute('aria-label', 'La muestra ha terminado');
  }

  function updateControls(index = pageFlip.getCurrentPageIndex()) {
    const page = Math.min(index + 1, PREVIEW_LAST_PAGE);
    const isSpread = pageFlip.getOrientation() === 'landscape' && page > 1 && page < PREVIEW_LAST_PAGE;
    counter.textContent = isSpread
      ? `Páginas ${page}–${Math.min(page + 1, 13)} de ${TOTAL_PAGES}`
      : `Página ${page} de ${TOTAL_PAGES}`;
    previous.disabled = index === 0 || isFlipping;
    next.disabled = isFlipping;
    next.innerHTML = index === 0
      ? 'Abrir libro <span aria-hidden="true">→</span>'
      : 'Siguiente <span aria-hidden="true">→</span>';
    next.setAttribute('aria-label', index === 0 ? 'Abrir la muestra' : 'Pasar a la siguiente página');
    finishPreview();
  }

  pageFlip.on('flip', ({ data }) => updateControls(data));
  pageFlip.on('changeOrientation', () => requestAnimationFrame(() => updateControls()));
  pageFlip.on('changeState', ({ data }) => {
    isFlipping = data === 'flipping';
    if (data === 'flipping' || data === 'read') updateControls();
  });
  pageFlip.loadFromHTML(pages);
  updateControls();

  function flipFromButton(direction) {
    // The library's click guard also applies to its own animated button API.
    const settings = pageFlip.getSettings();
    settings.disableFlipByClick = false;
    try {
      if (direction > 0) pageFlip.flipNext('bottom');
      else pageFlip.flipPrev('bottom');
    } finally {
      settings.disableFlipByClick = true;
    }
  }

  next.addEventListener('click', () => {
    stopSwipeCue();
    if (isFlipping || pageFlip.getCurrentPageIndex() >= PREVIEW_LAST_PAGE - 1) return;
    flipFromButton(1);
  });
  previous.addEventListener('click', () => {
    stopSwipeCue();
    if (!isFlipping && pageFlip.getCurrentPageIndex() > 0) flipFromButton(-1);
  });
  replay.addEventListener('click', () => {
    stopSwipeCue();
    if (isFlipping) return;
    pageFlip.turnToPage(0);
    updateControls(0);
  });

  [previous, next, replay].forEach((control) => {
    control.addEventListener('pointerdown', stopSwipeCue);
    control.addEventListener('keydown', stopSwipeCue);
  });

  bookElement.addEventListener('pointerdown', (event) => {
    stopSwipeCue();
    pointerStart = { id: event.pointerId, x: event.clientX, y: event.clientY };
  }, true);
  bookElement.addEventListener('pointermove', (event) => {
    if (!pointerStart || pointerStart.id !== event.pointerId) return;
    const distance = Math.hypot(event.clientX - pointerStart.x, event.clientY - pointerStart.y);
    if (distance > 14) suppressZoomUntil = performance.now() + 500;
  }, true);
  bookElement.addEventListener('pointerup', (event) => {
    if (pointerStart && pointerStart.id === event.pointerId) pointerStart = null;
  }, true);
  bookElement.addEventListener('pointercancel', () => {
    pointerStart = null;
  }, true);

  function openZoom(leaf) {
    if (!leaf || !zoom.showModal) return;
    const page = Number(leaf && leaf.dataset.page);
    if (!page || page >= PREVIEW_LAST_PAGE || isFlipping) return;
    const image = leaf.querySelector('img');
    zoomImage.src = image.src;
    zoomImage.alt = `Página ${page} ampliada del ebook`;
    zoom.showModal();
  }
  bookElement.addEventListener('click', (event) => {
    if (performance.now() < suppressZoomUntil) return;
    openZoom(event.target.closest('.preview-page'));
  });
  bookElement.addEventListener('keydown', (event) => {
    stopSwipeCue();
    if (event.key !== 'Enter' && event.key !== ' ') return;
    const leaf = event.target.closest('.preview-page');
    if (!leaf) return;
    event.preventDefault();
    openZoom(leaf);
  });
  byId('zoom-close').addEventListener('click', () => zoom.close());
  zoom.addEventListener('click', (event) => {
    if (event.target === zoom) zoom.close();
  });
  document.addEventListener('visibilitychange', () => {
    if (document.hidden && zoom.open) zoom.close();
  });
  watchSwipeCueVisibility();
  reducedMotion.addEventListener('change', ({ matches }) => {
    if (matches && swipeCueState === 'pending') {
      swipeCueState = 'suppressed';
      removeSwipeCueVisibilityWatch();
    } else if (matches && swipeCueState === 'active') {
      stopSwipeCue();
    }
    pageFlip.getSettings().flippingTime = matches ? 120 : 760;
  });
})();
